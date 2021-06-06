import subprocess
import re

from templates.colors import *

def Ping_the_host(host):

    try:
        regex_ip = f'{host} \((.*?)\)'
        regex_ttl = 'ttl=(.*?) '
        output = subprocess.run(f"ping -c 1 {host}",stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)

        if output.returncode == 0 or output.returncode == 1:

            print(f"{green}[+]THE HOST IS UP")
            output = output.stdout
            output = output.decode()
            ip = re.findall(regex_ip,output)[0]
            print(f"{yellow}[IP ADDRESS]---->{ip}")
            ttl = int(re.findall(regex_ttl,output)[0])
            print(f"{yellow}[TIME TO LIVE] ----> {ttl}s ")

            if ttl<100 :
                print(f"{yellow}THE HOST SERVER MOSTLY USING LINUX BASED OPERATION SYSTEM")
            elif 100<ttl<150:
                print("THE HOST SERVER MOSTLY USING WINDOWS BASED OPERATION SYSTEM")
            elif ttl>200:
                print("THE HOST SERVER MOSTLY USING SOLARIS BASED OPERATION SYSTEM")
            else :
                print(f"{red}OS DETECTION FAILED")        

        else :
            print(f"{red}[-]THE HOST IS DOWN OR SOMEPROBLEM WITH THE NETWORK CONNECTIVITY")

    except :
        pass
        


