#!/bin/env python
import cwiid
import atexit
import sys
import math
import socket
from time import sleep

acc_zero = None
acc_one = None
acc = [0, 0, 0]
leds = [1,2,4,8]

NEW_AMOUNT = 0.1
OLD_AMOUNT = 1 - NEW_AMOUNT

Roll_Scale = 1
Pitch_Scale = 1
X_Scale = 1
Y_Scale = 1
wm = None
sock = None
client = None

def start_wiimote():
    global acc_zero, acc_one, wm
    acc_zero, acc_one = wm.get_acc_cal(cwiid.EXT_NONE)
    wm.led=1

def setup_server_socket():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind( ("0.0.0.0", 25001) )
    sock.listen(1)

def report_acc_values(client):
    global wm, acc, acc_zero, acc_one
    axes = [None, None, None, None]
    wm.rpt_mode = cwiid.RPT_ACC
    current_led = 0
    next_led_update = 0

    while True:
        sleep(1.0 / 60.0)
        next_led_update+=1
        if(next_led_update > 60):
            next_led_update = 0
            current_led = (current_led + 1) % 4
            wm.led = leds[current_led]

        m = wm.state['acc']

        # Shamelessly "inspired" by
        # https://github.com/abstrakraft/cwiid/tree/master/wminput/plugins/acc/acc.py
        
        acc = [NEW_AMOUNT*(new-zero)/(one-zero) + OLD_AMOUNT*old
            for old,new,zero,one in zip(acc,m,acc_zero,acc_one)]
        a = math.sqrt(sum(map(lambda x: x**2, acc)))

        roll = math.atan(acc[cwiid.X]/acc[cwiid.Z])
        if acc[cwiid.Z] <= 0:
            if acc[cwiid.X] > 0: roll += math.pi
            else: roll -= math.pi

        pitch = math.atan(acc[cwiid.Y]/acc[cwiid.Z]*math.cos(roll))
#       print("WIIMOTE:%.2f:%.2f" % (pitch, roll))
        try:
            client.send("WIIMOTE:%.2f:%.2f" % (pitch, roll))
        except Exception:
            client.close()
            return

def connect_wiimote():
    global wm
    wm = None
    tries = 0
    
    print("Press 1+2 on WiiMote and press Enter")
    raw_input();

    while wm == None:
        print("Trying to connect... %d" % tries)
        wm = cwiid.Wiimote()
        tries+=1
        if(tries == 10):
            raise Exception("Can't connect")
    print("Connected!")

def cleanup():
    global wm, client

    if client != None:
        client.close()

    if wm != None:
        print("Closing connection...")
        wm.close()
        wm = None

def wait_for_clients():
    print("Waiting for client...")
    client,address = sock.accept()
    print("New client! %s" % str(address))
    report_acc_values(client)

if __name__=="__main__":
    atexit.register(cleanup)
    try:
        connect_wiimote()
    except Exception as e:
        print("Can't connect to WimMote!")
        sys.exit(1)

    start_wiimote()
    setup_server_socket()
    while True:
        wait_for_clients()

