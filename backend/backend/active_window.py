import sys
import os
import subprocess
import re

def get_active_window():
    stdout1, stderr1 = subprocess.Popen(['xdotool', 'getwindowfocus', 'getwindowname'], stdout=subprocess.PIPE).communicate()
    stdout2, stderr2 = subprocess.Popen(['xdotool', 'getwindowfocus', 'getwindowpid'], stdout=subprocess.PIPE).communicate()
    stdout3, stderr3 = subprocess.Popen(['ls', "-l", f"/proc/{stdout2.decode()[:-1]}/exe"], stdout=subprocess.PIPE).communicate()
    
    title = stdout1.decode()[:-1]
    app = stdout3.decode().split("/")[-1][:-1]
    return title, app
