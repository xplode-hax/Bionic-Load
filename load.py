# Bionic load - A simple Open source network & server monitoring tool XPLODE - ARX

# [ Start with our imports like always hhh
import os
import psutil
import subprocess
import json
import requests
import getpass
import time
import sys
import re
#]

try:
        interface = sys.argv[1] #Having an interface set as 1 by default like eth0 for all users will cause problems so let user choose their own
        refresh = int(sys.argv[2]) # I like having options.

except IndexError:
        print("[ERROR] <interface> <refresh> int(seconds) MISSING | No interface or time selected")
        print("Ex: python3 load.py eth0 1")
        sys.exit(1)

def main(interface,refresh): # top tier shkidded code.
   while(True):
       hidecursor = "\033[?25l" # hides the terminal cursor
       cores = psutil.cpu_count() # get core count
       cpuload = psutil.cpu_percent() # get cpu usage %
       cpu = subprocess.getoutput("grep -m 1 'model name' /proc/cpuinfo | cut -d: -f2 | sed -e 's/^ *//' | sed -e 's/$//'") # Grab cpu model name from /proc/cpuinfo
       ram = subprocess.getoutput("free -m | grep -oP '\d+' | head -n 1") # Get total ram 
       ep1 = subprocess.getoutput("ip route get 1.2.3.4 | awk '{print $7}'").strip() # get our ipv4
       uptime = subprocess.getoutput("uptime -p").replace("up","") # get our total uptime
       username = getpass.getuser() # username of logged in user
       Packets = subprocess.getoutput(r"grep "+ interface + ": /proc/net/dev | cut -d :  -f2 | awk '{ print $2 }'")
       bytes1file = open("/sys/class/net/"+ interface + "/statistics/rx_bytes", "r")
       bytes1 = bytes1file.read()
       bytes1file.close()
       time.sleep(1)
       Packets1 = subprocess.getoutput(r"grep "+ interface + ": /proc/net/dev | cut -d :  -f2 | awk '{ print $2 }'")
       pps = int(Packets) - int(Packets1)
       pps = str(pps)
       pps = pps.replace("-", "")
       bytes2file = open(f"/sys/class/net/{interface}/statistics/rx_bytes", "r")
       bytes2 = bytes2file.read()
       bytes1file.close()
       bytes2file.close()
       bytes1 = int(bytes1)
       bytes2 = int(bytes2)
       bbytes = bytes2 - bytes1
       mbps = bbytes / 125000
       conwatch = subprocess.getoutput(f"netstat -n --numeric-users --numeric-hosts") # getting a "sample" from netstat and then print only a small ammount on line 56
       estab1 = subprocess.getoutput("netstat -ant | grep ESTABLISHED | awk '{print $6}' | cut -d: -f1 | sort | uniq -c | sort -rn").strip()
       established = estab1.replace("ESTABLISHED","") # removing the part that says "ESTABLISHED" by replacing it with blank
       os.system("clear")
       print("\033[1m\x1b[47m\x1b[30m                   Bionic Load | Version 0.0.1 BETA | Arx/Xplode                \x1b[0m")
       print(f"""
Device {interface} | Address [{ep1}] | User: {username} | Uptime: {uptime}
==============================================================================
┌────────────────────────────────────────────────────────────────────────────
│ Server Info:
│ CPU Model: {cpu}
│ CPU Load: {cpuload}%
│ CPU Cores: {cores}
│
│ MBit/s: {mbps} | Packet/s: {pps}
│ Open TCP Connections: {established}
│ Netstat:
{conwatch[0:500]} 
{hidecursor}
       """)
       

       time.sleep(refresh) # Refresh stats

main(interface,refresh)
