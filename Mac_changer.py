#!usr/bin/env python

import time
import subprocess
import optparse
import random

def rand_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 127)*2,
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )

def change_add(interface, mac):
    print("[+] Changing Mac address to " + mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])
    return


def check():
    par = optparse.OptionParser()
    par.add_option("-i", "--interface", dest="interface", help="Interface to change")
    par.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    par.add_option("-r", "--random", dest="random", action="store_true", help="Random MAC address")
    par.add_option("-t", "--time", dest="time_interval", help="Time Interval(in sec) to change MAC address")

    (options,arguments) = par.parse_args()
    if not options.interface:
        par.error("[-] Please specify an interface")
    elif not options.new_mac:
        if not options.random:
            par.error("[-] Please specify MAC address")
        elif options.random:
            new_mac = rand_mac()
            if not options.time_interval:
                change_add(options.interface,new_mac)
            elif options.time_interval:
                while True:
                    change_add(options.interface,new_mac)
                    time1 = int(options.time_interval)
                    #print(time1)
                    time.sleep(time1)
                    new_mac = rand_mac()
        elif options.time_interval:
           par.error("[-] Cannot provide time unless random orientation is requested")
    elif options.new_mac:
        if options.time_interval:
            par.error("[-] Time interval can't be used while inserting MAC address manually")
        elif options.random:
            par.error("[-] Multiple MAC address given")
        else:
            change_add(options.interface,options.new_mac)
check()
