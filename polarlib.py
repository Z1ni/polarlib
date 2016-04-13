import usb.core
import usb.util
import struct
import datetime as dt
import deviceinfo   # For DEVICE.BPB
import physinfo     # For PHYSINFO.BPB
import dsum         # For DSUM.BPB

"""
Stuff for getting some data out from your Polar Loop (the first one, not tested
with Loop 2). Might work with other Polar devices (v800 and so).
Some methods are simple ports from v800_downloader
(https://github.com/profanum429/v800_downloader, see /src/usb/v800usb.cpp)
and some of the data models are from bipolar (https://github.com/pcolby/bipolar,
see /src/polar/v2/trainingsession.cpp)

Original source for methods __generate_request, __generate_ack, __add_to_full,
get_data, __is_end and __extract_dirs_and_files are Copyright 2014 Christian Weber.
See https://github.com/profanum429/v800_downloader, file /src/usb/v800usb.cpp

Some data models (deviceinfo, physinfo) are from bipolar, Copyright 2014-2016 Paul Colby.
See https://github.com/pcolby/bipolar, file /src/polar/v2/trainingsession.cpp

The remaining is Copyright 2016 Mark "zini" Mäkinen

    Polarlib
    Copyright (C) 2016 Mark "zini" Mäkinen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


TODO: Better exceptions
TODO: After a failed request the device ceases to respond
      E.g. One tries to retrieve nonexistant file, so the device returns empty response
           and stops responding after that. Can be fixed by replugging the device.
"""


class Directory:

    """Represents a directory

    Attributes:
        name    str     Directory name
        dirs    list    List of Directories (subdirs)
        files   list    List of Files
    """

    name = None
    dirs = []
    files = []

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Directory \"%s\": dirs: %s, files: %s" % (self.name, str(self.dirs), str(self.files))


class File:

    """Represents a file

    Attributes:
        name    str     Filename
    """

    name = None

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "File \"%s\"" % self.name


class Device:

    """Represents a device (e.g. Polar Loop)

    Attributes:
        pid             int                 Product ID (USB)
        serial          str                 Product serial from USB
        dev_info        DeviceInfo          DeviceInfo instance
        _usb_dev        usb.core.Device     The USB device
        _out_ep         usb.core.Endpoint   Out endpoint
        _in_ep          usb.core.Endpoint   In endpoint
        _packet_num     int                 Current packet number
    """

    pid = None
    serial = None

    dev_info = None

    _usb_dev = None
    _out_ep = None
    _in_ep = None

    _packet_num = 0

    def __init__(self, product_id):
        self.pid = product_id

    def connect(self):
        """Connects to the device (opens USB connection and gets device info)"""
        try:
            # For future reference: Polar Loop Product ID 0x0008
            self._usb_dev = usb.core.find(idVendor=0x0DA4, idProduct=self.pid)
        except usb.core.NoBackendError:
            raise Exception("Couldn't find a USB backend! Please install libusb!")

        if self._usb_dev is None:
            raise Exception("No device connected!")

        self.serial = usb.util.get_string(self._usb_dev, self._usb_dev.iSerialNumber)

        # Claim the device
        if self._usb_dev.is_kernel_driver_active(0):
            self._usb_dev.detach_kernel_driver(0)

        self._usb_dev.set_configuration()
        usb.util.claim_interface(self._usb_dev, 0)

        # Get the interface
        intf = self._usb_dev.get_active_configuration()[(0, 0)]

        # Get OUT and IN endpoints
        # TODO: Remove IN ep?
        self._out_ep = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
        self._in_ep = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

        # Get device info
        dev_info_raw = self.get_data("/DEVICE.BPB")
        self.dev_info = deviceinfo.DeviceInfo()
        self.dev_info.parse_from_bytes(dev_info_raw)

    def release(self):
        """Releases the USB device and the interface"""

        usb.util.release_interface(self._usb_dev, 0)

        if not self._usb_dev.is_kernel_driver_active(0):
            self._usb_dev.attach_kernel_driver(0)

        usb.util.dispose_resources(self._usb_dev)

    def __generate_request(self, req):
        """Generates a request to be sent to the device"""

        """
        Like this:
          packet[0] = 0x01
          packet[1] = ((request.length()+8) << 2)
          packet[2] = 0x00
          packet[3] = request.length() + 4
          packet[4] = 0x00
          packet[5] = 0x08
          packet[6] = 0x00
          packet[7] = 0x12
          packet[8] = len(request)
          packet += request.encode("utf-8")
        """
        packet = struct.pack("<BBBBBBBBB%ds" % (len(req)), 1, (len(req)+8) << 2, 0, len(req) + 4, 0, 8, 0, 0x12, len(req), req.encode("utf-8"))
        packet += b'\0' * (64 - len(packet))    # Padding

        return packet

    def __generate_ack(self):
        """Generates a ACK packet to be sent to the device"""
        packet = struct.pack("<BBB", 1, 5, self._packet_num)
        packet += b'\0' * (64 - len(packet))    # Padding
        return packet

    def __add_to_full(self, data, full, initial, final):
        """"Adds received data to the final buffer"""
        new_full = full
        size = data[1] >> 2

        # Trim the received data (headers, pad bytes)
        if initial:
            if final:
                size -= 4
            else:
                size -= 3

            data = data[5:]
            new_full += data[0:size]
        else:
            if final:
                size -= 2
            else:
                size -= 1

            data = data[3:]
            new_full += data[0:size]

        return new_full

    def get_data(self, req):
        """Requests data from the device and returns it after receiving it all"""

        run = True
        state = 0
        full = b""
        initial = True
        buf = b""
        self._packet_num = 0

        # State machine
        while run:
            if state == 0:
                # Generate and send the request
                packet = self.__generate_request(req)
                self._out_ep.write(packet)
                state = 1

            elif state == 1:
                # Read data from the device

                try:
                    buf = bytes(self._usb_dev.read(0x81, 64, 5000))
                except usb.core.USBError as e:
                    if e.errno == 110:
                        raise Exception("Read operation timed out! Reconnect device!")

                # Check if we have the last packet
                if self.__is_end(buf):
                    full = self.__add_to_full(buf, full, initial, True)
                    run = False
                else:
                    full = self.__add_to_full(buf, full, initial, False)
                    state = 2

                if initial:
                    initial = False

            elif state == 2:
                # Send ACK packet to get more data

                packet = self.__generate_ack()

                # Reset packet num counter if needed
                if (self._packet_num == 0xFF):
                    self._packet_num = 0
                else:
                    self._packet_num += 1

                self._out_ep.write(packet)
                state = 1

        return full

    def __is_end(self, packet):
        """Returns True if the given packet is the last one, otherwise False"""
        if (packet[1] & 0x03) == 1:
            return False
        else:
            return True

    def __extract_dirs_and_files(self, data):
        """Parses strings (names of dirs and files) from the given data"""
        state = 0
        size = 0
        loc = 0

        dirs_and_files = []

        while loc < len(data):
            if state == 0:
                if data[loc] == 0x0A:
                    # If we found 0x0A, continue searching for another one
                    loc += 1
                    state = 1
                loc += 1

            elif state == 1:
                if data[loc] == 0x0A:
                    # Now we have found two 0x0A bytes, move to the next step
                    state = 2
                else:
                    state = 0
                loc += 1

            elif state == 2:
                # Get the string size
                size = data[loc]
                state = 3
                loc += 1

            elif state == 3:
                # Get the string ending (0x10)
                if data[loc+size] == 0x10:
                    state = 4
                else:
                    state = 0

            elif state == 4:
                # Get the string and append it to the list
                name = data[loc:loc+size].decode("utf-8")
                dirs_and_files.append(name)
                state = 0
                loc += size

        return dirs_and_files

    def ls(self, path):
        """Gets somewhat sorted dir/filelisting for the given path

        Returns tuple that contains two lists (directories, files)
        """

        root_ls = self.get_data(path)
        # Here we sort the list by the last character of the name
        # This ensures that the directories are before files
        dirs_and_files = sorted(self.__extract_dirs_and_files(root_ls), key=lambda x: x[-1])

        dirs = []
        files = []

        # Directories end with /, files don't
        for entry in dirs_and_files:
            if entry[-1] == '/':
                d = Directory(entry)
                d.dirs, d.files = self.ls(path + entry)
                dirs.append(d)
            else:
                f = File(entry)
                files.append(f)

        return (dirs, files)

    def get_stats(self, date):
        """Gets some stats (e.g. step count) for the given date

        Returns an instance of Dsum
        """
        t_str = dt.datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")
        d = self.get_data("/U/0/%s/DSUM/DSUM.BPB" % t_str)
        if d == b"":
            return None

        ds = dsum.Dsum()
        ds.parse_from_bytes(d)

        return ds

    def get_physinfo(self):
        """Gets physical information about the user

        Returns an instance of PhysicalInformation
        """
        data = self.get_data("/U/0/S/PHYSDATA.BPB")

        pi = physinfo.PhysicalInformation()
        pi.parse_from_bytes(data)

        return pi
