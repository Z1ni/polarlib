# polarlib
Free your Polar Loop!

### What?
With polarlib, you can query files and data from your Polar Loop!

### Why?
Polar has the FlowSync application for Windows and Mac, but they have forgotten their Linux users!
This python module/app aims to create somewhat functional replacement for the FlowSync app.

### What does it need?
You need PyUSB and a USB library (libusb 0.1, libusb 1.0 or OpenUSB).

Quick how-to:
```
# apt-get install libusb-1.0-0
# pip install pyusb --pre
```
For more info, check out the PyUSB repo: <https://github.com/walac/pyusb>

### How to use?
This repo has a simple data query program called main.py (yeah, I should rename it).
It can show you information about your device, your physical information (!) and some data about currently saved days (step count and so on).

Run the program with the -h flag to see the available options.

And yes, you *need* to be root to use polarlib/programs that use it.
```
# ./main.py -h

Product ..: Polar Loop
Serial ...: xxxxxxxxx
Model ....: Unisex
Color ....: Black

Bootloader version ..: 1.1.7
Platform version ....: 0.9.5
Device version ......: 1.2.16
SVN revision ........: 120996
System ID ...........: xxxxxxxxxx
Hardware code .......: xxxxxxxxxx

Stats for 2016-04-13:
  Steps ....: 2229
  Time to go:
    Up .....: 06:09:00
    Walk ...: 01:50:00
    Jog ....: 00:48:00

```

### Thanks:
- Paul Colby ([@pcolby](https://github.com/pcolby)) for bipolar
- Christian Weber ([@profanum429](https://github.com/profanum429)) for v800_downloader

See [polarlib.py](polarlib.py) for more information.
