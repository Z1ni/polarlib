#!/usr/bin/env python3

import os
import sys
import datetime as dt
import polarlib
import physinfo
from argparse import ArgumentParser as AP

"""
Simple data query program for polarlib and Polar Loop (1).

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
"""


def print_dir(d, depth=0):
    print((" " * depth) + "%s" % d.name)
    for di in d.dirs:
        print_dir(di, depth + 1)
    for f in d.files:
        print((" " * (depth + 1)) + "%s" % f.name)


def ls_print(dev, path):
    d = polarlib.Directory(path)
    d.dirs, d.files = dev.ls(path)
    print_dir(d)


def print_dev_info(di):
    print("Product ..: %s" % di.model)
    print("Serial ...: %s" % di.serial)
    print("Model ....: %s" % di.design)
    print("Color ....: %s" % di.color)
    print()
    print("Bootloader version ..: %d.%d.%d" % (di.bootloaderVer.major, di.bootloaderVer.minor, di.bootloaderVer.patch))
    print("Platform version ....: %d.%d.%d" % (di.platformVer.major, di.platformVer.minor, di.platformVer.patch))
    print("Device version ......: %d.%d.%d" % (di.deviceVer.major, di.deviceVer.minor, di.deviceVer.patch))
    print("SVN revision ........: %d" % di.svnRev)
    print("System ID ...........: %s" % di.sysId)
    print("Hardware code .......: %s" % di.hwCode)
    print()


def print_phys_info(pi):
    usr_birthday = dt.date(pi.birthday.value.year, pi.birthday.value.month, pi.birthday.value.day)
    usr_last_modified = dt.datetime(pi.modified.date.year, pi.modified.date.month, pi.modified.date.day, pi.modified.time.hours, pi.modified.time.minutes, pi.modified.time.seconds)
    usr_gender = pi.gender.value
    usr_weight = pi.weight.value
    usr_height = pi.height.value

    print("User birthday .......: %s" % usr_birthday)
    print("User gender .........: %s" % ("Male" if usr_gender == physinfo.GenderOption.MALE else "Female"))
    print("User weight .........: %.2f kg" % usr_weight)
    print("User height .........: %.2f cm" % usr_height)
    print("Data last modified ..: %s" % usr_last_modified)
    print()


def print_stats(s):
    if s is None:
        print("No stats for %s" % args.stats_date)
        print("Please replug your device!")
        sys.exit(1)

    print("Stats for %s:" % args.stats_date)
    print("  Steps ....: %d" % s.steps)
    print("  Time to go:")
    print("    Up .....: %s" % dt.time(s.timeToGo.up.hours, s.timeToGo.up.minutes, s.timeToGo.up.seconds, s.timeToGo.up.milliseconds))
    print("    Walk ...: %s" % dt.time(s.timeToGo.walk.hours, s.timeToGo.walk.minutes, s.timeToGo.walk.seconds, s.timeToGo.walk.milliseconds))
    print("    Jog ....: %s" % dt.time(s.timeToGo.jog.hours, s.timeToGo.jog.minutes, s.timeToGo.jog.seconds, s.timeToGo.jog.milliseconds))


if __name__ == "__main__":

    # Check if we have root privileges
    try:
        if os.geteuid() != 0:
            print("You need root privileges to run this!")
            sys.exit(1)
    except AttributeError:
        print("Are you running this on Windows?")
        sys.exit(1)

    parser = AP(description="Polar Loop interface")
    parser.add_argument("-d", "--device-info", dest="dev_info", action="store_true", help="Display device info")
    parser.add_argument("-p", "--physical-info", dest="phys_info", action="store_true", help="Display user physical info")
    parser.add_argument("-s", "--stats", type=str, nargs="?", const=dt.date.today().strftime("%Y-%m-%d"), dest="stats_date", help="Display stats for the given day (yyyy-mm-dd) or empty if today")
    parser.add_argument("-l", "--ls", type=str, nargs="?", const="/", dest="ls", help="List files and folders from the given path (or empty if root)")
    parser.add_argument("--dump", type=str, help="Dump given file from the device")

    args = parser.parse_args()

    dev = polarlib.Device(0x0008)       # 0x0008 = Polar Loop
    dev.connect()

    if args.dev_info:
        print_dev_info(dev.dev_info)

    if args.phys_info:
        print_phys_info(dev.get_physinfo())

    if args.stats_date:
        print_stats(dev.get_stats(args.stats_date))

    if args.ls:
        print("Directory/file listing from \"%s\":" % args.ls)
        ls_print(dev, args.ls)

    if args.dump:
        print("Dumping file \"%s\"..." % args.dump)

        if args.dump[-1] == '/':
            print("Can't dump folders!")
            print("Please replug your device!")
            sys.exit(1)

        data = dev.get_data(args.dump)
        if data == b"":
            print("No such file!")
            print("Please replug your device!")
            sys.exit(1)

        f = open(os.path.basename(args.dump), "wb")
        f.write(data)
        f.close()
        print("Done.")

    dev.release()
