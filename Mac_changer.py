#!usr/bin/env python

import curses
import time
import subprocess
import optparse
import random
import re
import os

def rand_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 127) * 2,
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def current_mac(interface):
    config = subprocess.check_output(["ifconfig", interface])
    cur_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(config))[0]
    if cur_mac:
        return cur_mac
    else:
        print("[-] MAC address not found")


def change_add(interface, mac):
    subprocess.call(["ifconfig", interface, "down"], stdout=open(os.devnull, 'wb'))
    subprocess.call(["ifconfig", interface, "hw", "ether", mac], stdout=open(os.devnull, 'wb'))
    subprocess.call(["ifconfig", interface, "up"], stdout=open(os.devnull, 'wb'))
    new_mac_address = current_mac(interface)
    if new_mac_address:
        if new_mac_address == mac:
            return 1
    else:
        return 0


def check():
    par = optparse.OptionParser()
    par.add_option("-i", "--interface", dest="interface", help="Interface to change")
    par.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    par.add_option("-r", "--random", dest="random", action="store_true", help="Random MAC address")
    par.add_option("-t", "--time", dest="time_interval", help="Time Interval(in sec) to change MAC address")
    (options, arguments) = par.parse_args()
    if not options.interface:
        par.error("[-] Please specify an interface")
    elif not options.new_mac:
        if not options.random:
            par.error("[-] Please specify MAC address")
        elif options.random:
            new_mac = rand_mac()
            if not options.time_interval:
                print("[+] Changing Mac address to " + new_mac)
                cond0 = change_add(options.interface, new_mac)
                if cond0 == 1:
                    print("[+] MAC address changed succesfully")
                else:
                    print("[-] Error MAC address didn't change")
            else:
                stdscr = curses.initscr()
                curses.noecho()
                curses.cbreak()
                try:
                    while True:
                        condition = change_add(options.interface, new_mac)
                        stdscr.addstr(0, 0, "[+] Changing Mac address to {0}".format(new_mac))
                        if condition == 1:
                            stdscr.addstr(1, 0, "[+] MAC address changed succesfully")
                        else:
                            stdscr.addstr(1, 0, "[-] Error MAC address didn't change")
                        stdscr.refresh()
                        time1 = int(options.time_interval)
                        time.sleep(time1)
                        new_mac = rand_mac()
                except KeyboardInterrupt:
                    pass
                finally:
                    curses.echo()
                    curses.nocbreak()
                    curses.endwin()
        elif options.time_interval:
            par.error("[-] Cannot provide time unless random orientation is requested")
    elif options.new_mac:
        if options.time_interval:
            par.error("[-] Time interval can't be used while inserting MAC address manually")
        elif options.random:
            par.error("[-] Multiple MAC address given")
        else:
            print("[+] Changing Mac address to " + options.new_mac)
            cond1 = change_add(options.interface, options.new_mac)
            if cond1 == 1:
                print("[+] MAC address changed succesfully")
            else:
                print("[-] Error MAC address didn't change")


check()
