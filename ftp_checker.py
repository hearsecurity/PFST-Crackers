#!/usr/bin/python

import concurrent.futures
import sys
import ftplib
import requests

sshs = []

def open_port(ip):

    response = requests.get("http://"+ip, timeout=20)
    if  "Index of" in response.text:
       return True
    else:
       print "no-index"

def main_function(hostname):

    hostname = hostname.strip()
    userName = "anonymous"
    passWord = "anonymous"

    print "[+] Trying :" +hostname +""+ userName +"/" +passWord
    try:
        #value = open_port(hostname)
        #if value == True:
        ftp = ftplib.FTP(hostname)
        wellcome = ftp.getwelcome()
        #if  "Pure-FTPd" not in wellcome and "vsFTPd" not in wellcome:
        ftp.login(userName,passWord)
        print "\n[*]" +str(hostname) + "FTP Logon succeeded with"+userName+":"+passWord 
        ftp.quit()
        output = open('found.txt', 'a')
        output.write(hostname+":"+userName+":"+passWord+ "\n")
            #output.write(hostname+"\n")
        output.close()
        
    except Exception,e :
        print "error"
        
count = 0
with open(sys.argv[1]) as file:
    lines = file.readlines()
    for line in lines:
      count = count + 1
      sshs.append(line)


with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(main_function, sshs)
