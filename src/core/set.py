#!/usr/bin/env python
#########################################
#
# The Social-Engineer Toolkit
# Written by: David Kennedy (ReL1K)
# Email: davek@secmaniac.com
#
###############################################
import subprocess
import os
import time
import re
import sys
import socket
from src.core import setcore
from src.core.menu import text

###############################################
# Define path and set it to the SET root dir
###############################################

definepath = os.getcwd()
#os.chdir(definepath)
sys.path.append(definepath)

################################################
# ROOT CHECK
################################################

if os.geteuid() != 0:
        print "\n The Social-Engineer Toolkit (SET) - by David Kennedy (ReL1K)"
        print "\n Not running as root. \n\nExiting the Social-Engineer Toolkit (SET).\n"
        sys.exit(1)

setcore.check_pexpect()
setcore.check_beautifulsoup()
define_version = setcore.GetVersion()

# remove old stale files and restore java applet to original applet
setcore.cleanup_routine()

sys.path.append("../")
try:
   while 1:
     setcore.show_banner(define_version,'1')
     
    ###################################################
    #        USER INPUT: SHOW MAIN MENU               #
    ###################################################   

     show_main_menu = setcore.CreateMenu(text.main_text, text.main)
    
     # special case of list item 99
     print '\n  99) Return back to the main menu.\n'
     
     main_menu_choice = (raw_input(setcore.setprompt("0", "")))
     
     if main_menu_choice == 'exit':
		break         

     if main_menu_choice == '1': #'Spearphishing Attack Vectors
      while 1:
   
       ###################################################
       #        USER INPUT: SHOW SPEARPHISH MENU         #
       ###################################################   

       show_spearphish_menu = setcore.CreateMenu(text.spearphish_text, text.spearphish_menu)
       spearphish_menu_choice = raw_input(setcore.setprompt(["1"], ""))
       
       if spearphish_menu_choice == 'exit':
           setcore.ExitSet()
           
       if spearphish_menu_choice == 'help':
           print text.spearphish_text
       
       # Spearphish menu choice 1: Perform a Mass Email Attack
       if spearphish_menu_choice == '1':
           sys.path.append("src/core/msf_attacks/")
           try: reload(create_payload)
           except: pass
           import create_payload
       # Spearphish menu choice 2: Create a FileFormat Payload
       if spearphish_menu_choice == '2':
           sys.path.append("src/core/msf_attacks/")
           try: reload(create_payload)
           except: import create_payload   
       #Spearphish menu choice 3: Create a Social-Engineering Template
       if spearphish_menu_choice == '3':
                setcore.custom_template()
       #Spearphish menu choice 99
       if spearphish_menu_choice == '99': break

 #####################
 # Web Attack Menu
 #####################
     # Main Menu choice 2: Website Attack Vectors
     if main_menu_choice == '2':
      while 1:
        
        ###################################################
        #        USER INPUT: SHOW WEB ATTACK MENU         #
        ###################################################   

        show_webattack_menu = setcore.CreateMenu(text.webattack_text, text.webattack_menu)
        attack_vector = raw_input(setcore.setprompt(["2"], ""))
        
        if attack_vector == 'exit':
            setcore.ExitSet()

        if attack_vector == "":
            attack_vector = "1"

        # Web Attack menu choice 9: Create or Import a CodeSigning Certificate
        if attack_vector == '9':
            sys.path.append("src/html/unsigned")
            try: reload(verified_sign)
            except: import verified_sign
        # Web Attack menu choice 9: Return to the Previous Menu 
        if attack_vector == '99': break

        # Web Attack menu choice 7: Multi-Attack Web Method
        if attack_vector == "7":
            fileopen = file("config/set_config","r")
            for line in fileopen:
                line = line.rstrip()
                match = re.search("APACHE_SERVER=ON",line)
                if match:
                    setcore.PrintWarning("Apache mode is set to ON, you cannot use Multi-Attack Mode with Apache")
                    setcore.PrintWarning("Turn off APACHE_SERVER=ON in the SET_CONFIG and relaunch SET")
                    attack_vector = "30"

        try:
            attack_check = int(attack_vector)
        except: 
            setcore.PrintError("ERROR:Invalid selection, going back to menu.")
            break
        if attack_check > 9:
                raw_input("\n Invalid option. Press (return) to continue.")
                break
        # Web Attack menu choice 5: Man Left in the Middle Attack Method
        if attack_vector == "5": choice3='0'
        if attack_vector != "5":


                ###################################################
                #     USER INPUT: SHOW WEB ATTACK VECTORS MENU    #
                ###################################################   

                if attack_vector != "8":

                        show_webvectors_menu = setcore.CreateMenu(text.webattack_vectors_text, text.webattack_vectors_menu)
                        print '  99) Return to Webattack Menu\n'
                        choice3 = raw_input(setcore.setprompt(["2"], ""))
                
                        if choice3 == 'exit':
                            setcore.ExitSet()
                
                        if choice3 == "quit" or choice3 == '4': break

        
        try:
                # write our attack vector to file to be called later
                filewrite = file("src/program_junk/attack_vector","w")

                # webjacking and web templates are not allowed
                if attack_vector == "6" and choice3 == "1":
                        print setcore.bcolors.RED+ "\n Sorry, you can't use the Web Jacking vector with Web Templates."+ setcore.bcolors.ENDC
                        setcore.ReturnContinue()
                        break

                # if we select multiattack, web templates are not allowed
                if attack_vector == "7" and choice3 == "1":
                        print setcore.bcolors.RED+ "\n Sorry, you can't use the Multi-Attack vector with Web Templates." + setcore.bcolors.ENDC
                        setcore.ReturnContinue()
                        break

                # if we select web template and tabnabbing, throw this error and bomb out to menu
                if attack_vector == "4" and choice3 == "1":
                        print setcore.bcolors.RED+ "\n Sorry, you can only use the cloner option with the tabnabbing method." + setcore.bcolors.ENDC
                        setcore.ReturnContinue()
                        break

                # if attack vector is default or 1 for java applet
                if attack_vector == '': attack_vector = '1'
                # specify java applet attack
                if attack_vector == '1':
                        attack_vector = "java"
                        filewrite.write(attack_vector)
                        filewrite.close()

                # specify browser exploits
                if attack_vector == '2':
                        attack_vector = "browser"
                        filewrite.write(attack_vector)
                        filewrite.close()

                if attack_vector == '': attack_vector = '3'
                # specify web harvester method
                if attack_vector == '3':
                        attack_vector = "harvester"
                        filewrite.write(attack_vector)
                        filewrite.close()
                        setcore.PrintInfo("Email harvester will allow you to utilize the clone capabilities within SET")
                        setcore.PrintInfo("to harvest credentials or parameters from a website as well as place them into a report")

                # specify tab nabbing attack vector
                if attack_vector == '4':
                        attack_vector = "tabnabbing"
                        filewrite.write(attack_vector)
                        filewrite.close()

                # specify man left int he middle attack vector
                if attack_vector == '5':
                        attack_vector = "mlitm"
                        filewrite.write(attack_vector)
                        filewrite.close()

                # specify webjacking attack vector
                if attack_vector == "6":
                        attack_vector = "webjacking"
                        filewrite.write(attack_vector)
                        filewrite.close()

                # specify Multi-Attack Vector
                attack_vector_multi = ""
                if attack_vector == '7':
                        # trigger the multiattack flag in SET
                        attack_vector = "multiattack"
                        # write the attack vector to file
                        filewrite.write(attack_vector)
                        filewrite.close()

                # specify victim profiler
                if attack_vector == '8':
                        # trigger the victim profiler flag in SET
                        attack_vector = "profiler"
                        # write the attack vector to file
                        filewrite.write(attack_vector)
                        filewrite.close()
                        from src.webattack.profiler.webprofiler import *

                # pull ip address
                filewrite = file("src/program_junk/ipaddr.file","w")
                if choice3 != "5":
                        fileopen = file("config/set_config", "r").readlines()
                        for line in fileopen:
                                line = line.rstrip()
                                match = re.search("AUTO_DETECT=ON", line)
                                if match:
                                        try:
                                                ipaddr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                                ipaddr.connect(('google.com', 0))
                                                ipaddr.settimeout(2)
                                                ipaddr = ipaddr.getsockname()[0]
                                                filewrite.write(ipaddr)
                                                filewrite.close()
                                        except Exception, error:
                                                setcore.log(error)
                                                ipaddr = raw_input(setcore.setprompt(["2"], "Your interface IP Address"))
                                                filewrite.write(ipaddr)
                                                filewrite.close()

                        # if AUTO_DETECT=OFF prompt for IP Address
                        for line in fileopen:
                                line = line.rstrip()
                                match = re.search("AUTO_DETECT=OFF", line)
                                if match:
                                        if attack_vector != "harvester":
                                                if attack_vector != "tabnabbing":
                                                        if attack_vector != "webjacking":
                                                                # this part is to determine if NAT/port forwarding is used
                                                                # if it is it'll prompt for additional questions
                                                                setcore.PrintInfo("NAT/Port Forwarding can be used in the cases where your SET machine is")
                                                                setcore.PrintInfo("not externally exposed and may be a different IP address than your reverse listener.")
                                                                nat_or_fwd = raw_input(setcore.setprompt('0', 'Are you using NAT/Port Forwarding [yes|no]'))
                                                                if nat_or_fwd == "" or nat_or_fwd == "yes" or nat_or_fwd == "y":
                                                                        ipquestion = raw_input(setcore.setprompt(["2"], "IP address to SET web server (this could be your external IP or hostname)"))
                                                                        #while 1:
                                                                                # check if IP address is valid
                                                                                #ip_check = setcore.is_valid_ip(ipquestion)
                                                                                #if ip_check == False: ipquestion = raw_input("[!] Invalid ip address try again: ")
                                                                                #if ip_check == True: break

                                                                        filewrite2 = file("src/program_junk/interface", "w")
                                                                        filewrite2.write(ipquestion)
                                                                        filewrite2.close()
                                                                        # is your payload/listener on a different IP?
                                                                        natquestion = raw_input(setcore.setprompt(["2"], "Is your payload handler (metasploit) on a different IP from your external NAT/Port FWD address [yes|no]"))
                                                                        if natquestion == 'yes' or natquestion == 'y':
                                                                                ipaddr=raw_input(setcore.setprompt(["2"], "IP address for the reverse handler (reverse payload)"))
                                                                        if natquestion == "" or natquestion == "n" or natquestion == "no":
                                                                                ipaddr = ipquestion
                                                                # if you arent using NAT/Port FWD
                                                                if nat_or_fwd == "" or nat_or_fwd == "no" or nat_or_fwd == "n":
                                                                        setcore.PrintInfo("Enter the IP address of your interface IP or if your using an external IP, what")
                                                                        setcore.PrintInfo("will be used for the connection back and to house the web server (your interface address)")
                                                                        ipaddr = raw_input(setcore.setprompt(["2"], "IP address for the reverse connection"))
        
                                        if attack_vector == "harvester" or attack_vector == "tabnabbing" or attack_vector == "webjacking":
                                                setcore.PrintInfo("This option is used for what IP the server will POST to.")
                                                setcore.PrintInfo("If you're using an external IP, use your external IP for this")
                                                ipaddr = raw_input(setcore.setprompt(["2"], "IP address for the POST back in Harvester/Tabnabbing"))
                                        filewrite.write(ipaddr)
                                        filewrite.close()

                        # if java applet attack
                        if attack_vector == "java":
                                # Allow Self-Signed Certificates
                                fileopen = file("config/set_config", "r").readlines()
                                for line in fileopen:
                                        line = line.rstrip()
                                        match = re.search("SELF_SIGNED_APPLET=ON", line)
                                        if match:
                                                sys.path.append("src/html/unsigned/")
                                                import self_sign

                # Select SET quick setup
                if choice3 == '1':

                                # get the template ready
                                sys.path.append("src/html/templates")
                                try: reload(template)
                                except: import template

                                # grab browser exploit selection
                                if attack_vector == "browser":
                                        # grab clientattack
                                        sys.path.append("src/webattack/browser_exploits")
                                        try: reload(gen_payload)
                                        except: import gen_payload

                                # arp cache attack, will exit quickly 
                                # if not in config file
                                sys.path.append("src/core/arp_cache")
                                try: reload(arp_cache)
                                except: import arp_cache
                                # actual website attack here
                                # web_server.py is main core 
                                sys.path.append("src/html/")
                                # clean up stale file
                                subprocess.Popen("rm src/program_junk/cloner.failed 1> /dev/null 2> /dev/null", shell = True).wait()

                                site_cloned = True

                                sys.path.append("src/webattack/web_clone/")
                                try: reload(cloner)
                                except: import cloner


                                # grab java applet attack
                                if attack_vector == "java":
                                        # create payload here
                                        sys.path.append("src/core/payloadgen")
                                        try: reload(create_payloads)
                                        except: import create_payloads

                                if os.path.isfile("src/program_junk/cloner.failed"):
                                        site_cloned = False

                                if site_cloned == True:

                                        # cred harvester for auto site here
                                        if attack_vector == "harvester" or attack_vector == "tabnabbing" or attack_vector == "webjacking":
                                                if attack_vector == "tabnabbing" or attack_vector == "webjacking":
                                                        sys,path.append("src/webattack/tabnabbing")
                                                        try:reload(tabnabbing)
                                                        except: import tabnabbing
                                                # start web cred harvester here
                                                sys.path.append("src/webattack/harvester")
                                                try: reload(harvester)
                                                except: import harvester
        
                                        # if we are using profiler lets prep everything to get ready
                                        if attack_vector == "profiler":
                                                from src.webattack.profiler.webprofiler import *
                                                prep_website()

                                        if attack_vector != "harvester":
                                            if attack_vector != "tabnabbing":
                                                if attack_vector != "multiattack":
                                                    if attack_vector != "webjacking":
                                                        if attack_vector != "multiattack":
                                                            if attack_vector != "profiler":
                                                                    # spawn web server here
                                                                    try: reload(spawn)
                                                                    except: import spawn


                                        # multi attack vector here
                                        if attack_vector =="multiattack":
                                            if choice3 == "1":
                                                try:
                                                    filewrite = file("src/progam_junk/multiattack.template","w")
                                                    filewrite.write("TEMPLATE=TRUE")
                                                    filewrite.close()
                                                except: pass
                                                sys.path.append("src/webattack/multi_attack/")
                                                try: reload(multiattack)
                                                except: import multiattack


                # Create a website clone
                if choice3 == '2':
                        # flag that we want a custom website
                        sys.path.append("src/webattack/web_clone/")
                        if os.path.isfile("src/program_junk/site.template"):
                                subprocess.Popen("rm src/program_junk/site.template", shell = True).wait()
                        filewrite = file("src/program_junk/site.template", "w")
                        filewrite.write("TEMPLATE=CUSTOM")
                        setcore.PrintInfo("SET supports both HTTP and HTTPS")

                        # specify the site to clone
                        setcore.PrintInfo("Example: http://www.thisisafakesite.com")
                        URL = raw_input(setcore.setprompt(["2"], "Enter the url to clone"))
                        match = re.search("http://", URL)
                        match1 = re.search("https://", URL)
                        if not match:
                                if not match1:
                                        URL = ("http://"+URL)

                        match2 = re.search("facebook.com", URL)
                        if match2:
                                URL = ("https://login.facebook.com/login.php")

                        filewrite.write("\nURL=%s" % (URL))
                        filewrite.close()

                        # grab browser exploit selection
                        if attack_vector == "browser":
                                   # grab clientattack
                                   sys.path.append("src/webattack/browser_exploits")
                                   try: reload(gen_payload)
                                   except: import gen_payload

                        # set site cloner to true
                        site_cloned = True

                        if attack_vector != "multiattack":
                                # import our website cloner

                                site_cloned = True

                                try: reload(cloner)
                                except: import cloner

                                if os.path.isfile("src/program_junk/cloner.failed"):
                                        site_cloned = False

                        if site_cloned == True:

                                if attack_vector == "java":
                                        # import our payload generator
                                        sys.path.append("src/core/payloadgen/")
                                        try: reload(create_payloads)
                                        except: import create_payloads

                                # arp cache if applicable
                                sys.path.append("src/core/arp_cache")
                                try: reload(arp_cache)
                                except: import arp_cache

                                # tabnabbing and harvester selection here
                                if attack_vector == "harvester" or attack_vector == "tabnabbing" or attack_vector == "webjacking":
                                        if attack_vector == "tabnabbing" or attack_vector == "webjacking":
                                                sys.path.append("src/webattack/tabnabbing")
                                                try: reload(tabnabbing)
                                                except: import tabnabbing
                                        sys.path.append("src/webattack/harvester")
                                        try: reload(harvester)
                                        except: import harvester

                                # multi_attack vector here
                                if attack_vector == "multiattack":
                                        sys.path.append("src/webattack/multi_attack/")
                                        try: reload(multiattack)
                                        except: import multiattack

                                # if we arent using credential harvester or tabnabbing
                                if attack_vector != "harvester":
                                        if attack_vector != "tabnabbing":
                                                if attack_vector != "multiattack":
                                                        if attack_vector != "webjacking":
                                                                sys.path.append("src/html")
                                                                try: reload(spawn)
                                                                except: import spawn

                # Import your own site
                if choice3 == '3':
                        sys.path.append("src/webattack/web_clone/")
                        if os.path.isfile("src/program_junk/site.template"):
                                subprocess.Popen("rm src/program_junk/site.template", shell = True).wait()
                        filewrite = file("src/program_junk/site.template", "w")
                        filewrite.write("TEMPLATE=SELF")
                        # specify the site to clone
                        if not os.path.isdir("src/program_junk/web_clone"):
                                subprocess.Popen("mkdir src/program_junk/web_clone", shell=True)
                        setcore.PrintWarning("Example: /home/website/ (make sure you end with /)")
                        setcore.PrintWarning("Also note that there MUST be an index.html in the folder you point to.")
                        URL = raw_input(setcore.setprompt(["2"], "Path to the website to be cloned"))
                        if not os.path.isfile(URL+"index.html"):
                                if os.path.isfile(URL):
                                        subprocess.Popen("cp %s %s/src/program_junk/web_clone/index.html" % (URL,definepath), shell=True).wait()
                                if not os.path.isfile(URL):
                                        setcore.PrintError("ERROR:index.html not found!!")
                                        setcore.PrintError("ERROR:Did you just put the path in, not file?")
                                        setcore.PrintError("Exiting the Social-Engineer Toolkit...Hack the Gibson.\n")
                                        setcore.ExitSet()
                        if os.path.isfile(URL+"index.html"):
                                URL = URL + "index.html"
                        subprocess.Popen("cp %s src/program_junk/web_clone/" % (URL), shell = True).wait()
                        filewrite.write("\nURL=%s" % (URL))
                        filewrite.close()
                        
                        # if not harvester then load up cloner
                        if attack_vector == "java" or attack_vector == "browser":        
                                 # import our website cloner
                                 try: reload(cloner)
                                 except: import cloner

                        # if java applet attack
                        if attack_vector == "java":
                                # import our payload generator
                                sys.path.append("src/core/payloadgen/")
                                try: reload(create_payloads)
                                except: import create_payloads

                        # grab browser exploit selection
                        if attack_vector == "browser":
                            # grab clientattack
                            sys.path.append("src/webattack/browser_exploits")
                            try: reload(gen_payload)
                            except: import gen_payload

                        # arp cache if applicable
                        sys.path.append("src/core/arp_cache")
                        try: reload(arp_cache)
                        except: import arp_cache

                        # if not harvester spawn server
                        if attack_vector == "java" or attack_vector == "browser":
                                # import web_server and do magic
                                sys.path.append("src/html")
                                try: reload(spawn)
                                except: import spawn

                        # cred harvester for auto site here
                        if attack_vector == "harvester":
                                # get the url
                                setcore.PrintInfo("Example: http://www.blah.com")
                                URL = raw_input(setcore.setprompt(["2"], "URL of the website you imported"))
                                match = re.search("http://", URL)
                                match1 = re.search("https://", URL)
                                if not match:
                                        if not match1:
                                                URL = ("http://"+URL)
                                filewrite = file("src/program_junk/site.template","w")
                                filewrite.write("\nURL=%s" % (URL))
                                filewrite.close()

                                # start web cred harvester here
                                sys.path.append("src/webattack/harvester")
                                try: reload(harvester)
                                except: import harvester

                        # tabnabbing for auto site here
                        if attack_vector == "tabnabbing" or attack_vector == "webjacking":
                                # get the url
                                setcore.PrintInfo("Example: http://www.blah.com")
                                URL = raw_input(setcore.setprompt(["2"], "URL of the website you imported"))
                                match = re.search("http://", URL)
                                match1 = re.search("https://", URL)
                                if not match:
                                        if not match1:
                                                URL = ("http://"+URL)
                                filewrite = file("src/program_junk/site.template","w")
                                filewrite.write("\nURL=%s" % (URL))
                                filewrite.close()
                                # start tabnabbing here
                                sys.path.append("src/webattack/tabnabbing")
                                try: reload(tabnabbing)
                                except: import tabnabbing

                                # start web cred harvester here
                                sys.path.append("src/webattack/harvester")
                                try: reload(harvester)
                                except: import harvester

                # option for thebiz man left in the middle attack vector
                if choice3 == '0':
                        sys.path.append("src/webattack/mlitm")
                        try: reload(thebiz)
                        except: import thebiz

                # Return to main menu
                if choice3 == '4':
                        print (" Returning to main menu.\n")        
                        break
        except KeyboardInterrupt:
                print " Control-C detected, bombing out to previous menu.."
                break

     # Define Auto-Infection USB/CD Method here
     if main_menu_choice == '3':
        
        ###################################################
        #     USER INPUT: SHOW INFECTIOUS MEDIA MENU      #
        ###################################################   
        # Main Menu choice 3: Infectious Media Generator
        
        show_infectious_menu = setcore.CreateMenu(text.infectious_text, text.infectious_menu)
        infectious_menu_choice = raw_input(setcore.setprompt(["3"], ""))

        if infectious_menu_choice == 'exit':
            setcore.ExitSet()

        if infectious_menu_choice == "99":
            setcore.menu_back()
            
        if infectious_menu_choice == "":
            infectious_menu_choice = "1"
                    
        # if fileformat
        if infectious_menu_choice == "1":
                ipaddr = raw_input(setcore.setprompt(["3"], "IP address for the reverse connection (payload)"))
                filewrite = file("src/program_junk/ipaddr.file", "w")
                filewrite.write(ipaddr)
                filewrite.close
        filewrite1 = file("src/program_junk/payloadgen", "w")
        filewrite1.write("payloadgen=solo")
        filewrite1.close()

        # if choice is file-format
        if infectious_menu_choice == "1":
                filewrite = file("src/program_junk/fileformat.file","w")
                filewrite.write("fileformat=on")
                filewrite.close()
                sys.path.append("src/core/msf_attacks/")
                try: reload(create_payload)
                except: import create_payload

        # if choice is standard payload
        if infectious_menu_choice == "2":
                filewrite = file("src/program_junk/standardpayload.file", "w")
                filewrite.write("standardpayload=on")
                filewrite.close()
                sys.path.append("src/core/payloadgen/")
                try: reload(create_payloads)
                except: import create_payloads

        if infectious_menu_choice != "99":
                # import the autorun stuff
                sys.path.append("src/autorun/")
                try: reload(autorun)
                except: import autorun

        if infectious_menu_choice == "2":
                sys.path.append("src/core/payloadgen/")
                try: reload(solo)
                except: import solo

     # Main Menu choice 4: Create a Payload and Listener     
     if main_menu_choice == '4':
        filewrite = file("src/program_junk/payloadgen", "w")
        filewrite.write("payloadgen=solo")
        filewrite.close()
        sys.path.append("src/core/payloadgen/")
        try: reload(create_payloads)
        except: import create_payloads
        setcore.PrintStatus("Your payload is now in the root directory of SET as msf.exe")
        if os.path.isfile("src/program_junk/meterpreter.alpha"):
                print "[*] Saving alphanumeric shellcode in root directory of SET as meterpreter.alpha"
                subprocess.Popen("cp src/program_junk/meterpreter.alpha ./", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        subprocess.Popen("cp src/html/msf.exe ./msf.exe 1> /dev/null 2> /dev/null", shell = True).wait()
        
        # if we didn't select the SET interactive shell or RATTE
        if not os.path.isfile("src/program_junk/set.payload"):
                setcore.upx("msf.exe")

        # if the set payload is there
        if os.path.isfile("src/program_junk/set.payload"):
                subprocess.Popen("cp src/program_junk/msf.exe ./msf.exe 1> /dev/null 2> /dev/null", shell = True).wait()

        try: reload(solo)
        except: import solo
        raw_input("\nPress " + setcore.bcolors.RED + "{return}" + setcore.bcolors.ENDC + " to head back to the menu.")

     # Main Menu choice 5: Mass Mailer Attack
     if main_menu_choice == '5':
        sys.path.append("src/phishing/smtp/client")
        try: reload(smtp_web)
        except: import smtp_web

     # Main Menu choice 6: Teensy USB HID Attack Vector
     if main_menu_choice == '6':
        
        ###################################################
        #        USER INPUT: SHOW TEENSY MENU             #
        ###################################################   
        show_teensy_menu = setcore.CreateMenu(text.teensy_text, text.teensy_menu)
        teensy_menu_choice = raw_input(setcore.setprompt(["6"], ""))

        if teensy_menu_choice == 'exit':
            setcore.ExitSet()

        # if not return to main menu
        yes_or_no = ''

        if teensy_menu_choice != "99":
                # set our teensy info file in program junk
                filewrite = file("src/program_junk/teensy", "w")
                filewrite.write(teensy_menu_choice+"\n")
                if teensy_menu_choice != "3" and teensy_menu_choice != "7" and teensy_menu_choice !="8" and teensy_menu_choice !="9" and teensy_menu_choice !="10" and teensy_menu_choice != "11" and teensy_menu_choice != "12":
                        yes_or_no = raw_input(" Do you want to create a payload and listener [yes|no]: ")
                        if yes_or_no == "yes" or yes_or_no == "y" or yes_or_no == "":
                                filewrite.write("payload")
                                filewrite.close()
                                # load a payload
                                sys.path.append("src/core/payloadgen")
                                try: reload(create_payloads)
                                except: import create_payloads
                if yes_or_no == "no" or yes_or_no == "n":
                        filewrite.close()
                # need these default files for web server load
                filewrite = file("src/program_junk/site.template", "w")
                filewrite.write("TEMPLATE=CUSTOM")
                filewrite.close()
                filewrite = file("src/program_junk/attack_vector", "w")
                filewrite.write("hid")
                filewrite.close()
                # if we are doing binary2teensy
                if teensy_menu_choice != "7" and teensy_menu_choice !="8" and teensy_menu_choice != "9" and teensy_menu_choice !="10" and teensy_menu_choice != "11" and teensy_menu_choice != "12":
                        sys.path.append("src/teensy")
                        try: reload(teensy)
                        except: import teensy
                if teensy_menu_choice == "7":
                        import src.teensy.binary2teensy
                # if we are doing sd2teensy attack
                if teensy_menu_choice == "8":
                        import src.teensy.sd2teensy

                # if we are doing the sd2teensy osx attack
                if teensy_menu_choice == "9":
                        setcore.PrintStatus("Generating the SD2Teensy OSX pde file for you...")
                        subprocess.Popen("cp src/teensy/osx_sd2teensy.pde reports/ 1> /dev/null 2>/dev/null", shell=True).wait()
                        setcore.PrintStatus("File has been exported to reports/osx_sd2teensy.pde")
                        setcore.ReturnContinue()

                # if we are doing the X10 Arduino Sniffer
                if teensy_menu_choice == "10":
                        setcore.PrintStatus("Generating the Arduino sniffer and libraries pde..")
                        subprocess.Popen("mkdir reports/arduino_sniffer 1> /dev/null 2>/dev/null;cp src/teensy/x10/x10_sniffer.pde ./reports/arduino_sniffer 1> /dev/null 2> /dev/null;cp src/teensy/x10/libraries.zip ./reports/arduino_sniffer/ 1> /dev/null 2> /dev/null", shell=True).wait()
                        setcore.PrintStatus("Arduino sniffer files and libraries exported to reports/arduino_sniffer")
                        setcore.ReturnContinue()

                # if we are doing the X10 Jammer
                if teensy_menu_choice == "11":
                        setcore.PrintStatus("Generating the Arduino jammer pde and libraries...")
                        subprocess.Popen("mkdir reports/arduino_jammer 1> /dev/null 2>/dev/null;cp src/teensy/x10/x10_blackout.pde ./reports/arduino_jammer 1> /dev/null 2>/dev/null;cp src/teensy/x10/libraries.zip ./reports/arduino_jammer/ 1> /dev/null 2> /dev/null", shell=True).wait()
                        setcore.PrintStatus("Arduino jammer files and libraries exported to reports/arduino_jammer")
                        setcore.ReturnContinue()

                # powershell shellcode injection
                if teensy_menu_choice == "12":
                        setcore.PrintStatus("Generating the Powershell - Shellcode injection pde..")
                        import src.teensy.powershell_shellcode
                
        if teensy_menu_choice == "99": teensy_menu_choice = None

     #
     # Main Menu choice 8: Wireless Attack Point Attack Vector
     #
     if main_menu_choice == '8':

                # set path to nothing
                airbase_path = ""
                dnsspoof_path = ""
                # need to pull the SET config file
                fileopen = file("config/set_config", "r")
                for line in fileopen:
                        line = line.rstrip()
                        match = re.search("AIRBASE_NG_PATH=", line)
                        if match:
                                airbase_path = line.replace("AIRBASE_NG_PATH=", "")

                        match1 = re.search("DNSSPOOF_PATH=", line)
                        if match1: dnsspoof_path = line.replace("DNSSPOOF_PATH=", "")

                if not os.path.isfile(airbase_path):
                        if not os.path.isfile("/usr/local/sbin/airbase-ng"):
                                setcore.PrintWarning("Warning airbase-ng was not detected on your system. Using one in SET.")
                                setcore.PrintWarning("If you experience issues, you should install airbase-ng on your system.")
                                setcore.PrintWarning("You can configure it through the set_config and point to airbase-ng.")
                                airbase_path = ("src/wireless/airbase-ng")
                        if os.path.isfile("/usr/local/sbin/airbase-ng"): 
                                airbase_path = "/usr/local/sbin/airbase-ng"

                if not os.path.isfile(dnsspoof_path):
                        if os.path.isfile("/usr/local/sbin/dnsspoof"): dnsspoof_path = "/usr/local/sbin/dnsspoof"

                # if we can find airbase-ng
                if os.path.isfile(airbase_path):
                        if os.path.isfile(dnsspoof_path):
                                # start the menu here
                                while 1:
                                        
                                        ###################################################
                                        #        USER INPUT: SHOW WIRELESS MENU           #
                                        ###################################################   

                                        show_wireless_menu = setcore.CreateMenu(text.wireless_attack_text, text.wireless_attack_menu)
                                        wireless_menu_choice = raw_input(setcore.setprompt(["8"], ""))
                                        # if we want to start access point
                                        if wireless_menu_choice == "1":                
                                                sys.path.append("src/wireless/")
                                                try: reload(wifiattack)
                                                except: import wifiattack

                                        # if we want to stop the wifi attack
                                        if wireless_menu_choice == "2":
                                                sys.path.append("src/wireless/")
                                                try: reload(stop_wifiattack)
                                                except: import stop_wifiattack

                                        # if we want to return to the main menu
                                        if wireless_menu_choice == "99":
                                                print (" [*] Returning to the main menu ...")
                                                break
                
                if not os.path.isfile(dnsspoof_path):
                                if not os.path.isfile("/usr/local/sbin/dnsspoof"):
                                        setcore.PrintError("ERROR:DNS Spoof was not detected. Check the set_config file.")
                                        setcore.ReturnContinue()

     # 
     # END WIFI ATTACK MODULE
     #

     # Main Menu choice 9: Third Pary Modules
     if main_menu_choice == '9':
        sys.path.append("src/core")
        try: reload(module_handler)
        except: import module_handler

     # Main Menu choice 99: Exit the Social-Engineer Toolkit
     if main_menu_choice == '99': 
        #print "\n Thank you for "+ setcore.bcolors.RED+"shopping" + setcore.bcolors.ENDC+" at the Social-Engineer Toolkit.\n\n Hack the Gibson...and remember...hugs are worth more than handshakes.\n"
        #subprocess.Popen("killall python 1> /dev/null 2> /dev/null", shell = True).wait()
        #sys.exit(1)
	break

     # Main Menu choice 7: SMS Spoofing Attack Vector
     if main_menu_choice == '7':
        sms_menu_choice = '0'
        while sms_menu_choice != '3':
                
                ###################################################
                #        USER INPUT: SHOW SMS MENU                #
                ###################################################   

                show_sms_menu = setcore.CreateMenu(text.sms_attack_text, text.sms_attack_menu)
                sms_menu_choice=raw_input(setcore.setprompt(["7"], ""))
                
                if sms_menu_choice == 'exit':
                    setcore.ExitSet()
                        
                if sms_menu_choice == '1':
                        sys.path.append("src/sms/client/")
                        try: reload(sms_client)
                        except: import sms_client 
                
                if sms_menu_choice == '2':
                        sys.path.append("src/sms/client/")
                        try: reload(custom_sms_template)
                        except: import custom_sms_template
                
                if sms_menu_choice == '99': break

# handle keyboard interrupts
except KeyboardInterrupt: 
        print "\n\n Thank you for " + setcore.bcolors.RED+"shopping" + setcore.bcolors.ENDC+" at the Social-Engineer Toolkit.\n\n Hack the Gibson...and remember...hugs are worth more than handshakes.\n"

# handle exceptions
except Exception, error:
        setcore.log(error)
        print "\n\n Something went wrong, printing the error: "+ str(error)
