#!/usr/bin/env python

import subprocess
from src.core import setcore

#
# Simple python script to kill things created by the SET wifi attack vector
#

interface = raw_input(setcore.setprompt(["8"], "Enter your wireless interface (ex: wlan0): "))

# fix a bug if present
setcore.PrintStatus("Attempting to set rfkill to unblock all if RTL is in use. Ignore errors on this.")
subprocess.Popen("rmmod rtl8187;rfkill block all;rfkill unblock all;modprobe rtl8187;rfkill unblock all;ifconfig %s up" % (interface), shell=True).wait()

setcore.PrintStatus("Killing airbase-ng...")
subprocess.Popen("killall airbase-ng", shell=True).wait()

setcore.PrintStatus("Killing dhcpd3 and dhclient3...")
subprocess.Popen("killall dhcpd3", shell=True).wait()
subprocess.Popen("killall dhclient3", shell=True).wait()

setcore.PrintStatus("Killing dnsspoof...")
subprocess.Popen("killall dnsspoof", shell=True).wait()

setcore.PrintStatus("Turning off IP_forwarding...")
subprocess.Popen("echo 0 > /proc/sys/net/ipv4/ip_forward", shell=True).wait()

setcore.PrintStatus("Killing monitor mode on mon0...")
subprocess.Popen("src/wireless/airmon-ng stop mon0", shell=True).wait()

setcore.PrintStatus("Turning off monitor mode on wlan0...")
subprocess.Popen("src/wireless/airmon-ng stop wlan0", shell=True).wait()

setcore.PrintStatus("SET has stopped the wireless access point. ")
setcore.ReturnContinue()