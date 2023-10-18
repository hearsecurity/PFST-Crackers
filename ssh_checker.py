#!/usr/bin/python

from pexpect import pxssh
import concurrent.futures
import socket
import sys

sshs = []

def port_checker(ssh):

    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(10)
      s.connect((ssh, 22))
      return True
    except:
      time.sleep(1)
    finally:
      s.shutdown(socket.SHUT_RDWR)
      s.close()


def main_function(sshs):

    sshs = sshs.strip()

    item = sshs.split(":")
    ssh = item[0]
    login = item[1]
    password = item[2]
        
    print "Trying: "+ssh+" Login: "+login+" Password: "+password
    
    try:
        s = pxssh.pxssh(timeout=60)
        s.PROMPT= 'SSH>'
        if not s.login (ssh, login, password, auto_prompt_reset=False):
            print "SSH session failed on login."
            print str(s)
        else:
            print "SSH session login successful"
            s.sendline ('uname -a')
            s.prompt()         # match the prompt
            s.expect('[#\$] ')
            

            if port_checker(ssh):
                  output = open('found.txt', 'a')
                  output.write(ssh+":"+login+":"+password + "\n")
                  output.close()
            
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)
        
count = 0
with open(sys.argv[1]) as file:
    lines = file.readlines()
    for line in lines:
      count = count + 1
      sshs.append(line)


with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(main_function, sshs)
