import subprocess
from templates.colors import red , reset , green

def SPF(domain):

    print("[+][#### SPF VULNERABILITY CHECKING ####]\n")
    try:
        spf = subprocess.check_output(f"host -t TXT {domain}" ,shell=True)
    
        if "spf" not in spf.decode():
            print(f"{red}[-]POSSIBLE SPF VULNERABILITY NO TXT RECORDS FOUND{reset}")
    
        else :      
            print(f"{green}[+]TXT RECORDS FOR THE DOMAIN{reset}\n"+spf.decode())
    
    except Exception as e:
        print(f"\tsomething went wrong while getting txt records for {domain}\n\n"+str(e))
        

