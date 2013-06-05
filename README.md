Python WiiMote Server
===============

Python script that serves WiiMote data over the network.

Dependencies
-------------
Pywiimoteserves uses the cwiid python binding. On a Debian/Ubuntu system you can install it with

    sudo apt-get install python-cwiid

How to run it
-------------
This is just a python program:

    python pywiimoteserver.py

How to use it
-------------
Just connect to the server (port 25001 by default) and start receiving data. The format is pretty silly right now:
    
    WIIMOTE:PITCH_VALUE:ROLL_VALUE

This is what I need right now and it's easy as pie to adapt it for any need you may have.

License
--------
Do whatever you want with this, but don't blame me.

