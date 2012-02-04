#!/usr/bin/python
import os
import sys
definepath=os.getcwd()
sys.path.append(definepath)
from src.core import setcore
setcore.start_web_server_unthreaded("src/program_junk/web_clone/")

