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

Beware that right now the server is a one-use-app. When then client disconnects, you need to restart the server. I'll work on fixing this some day...

License
--------
Do whatever you want with this, but don't blame me.

