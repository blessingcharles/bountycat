import requests
from bs4 import BeautifulSoup
from random import choice

r = requests.get("https://sslproxies.org/")
soup = BeautifulSoup(r.content,"html5lib")
ip =map(lambda x:x.text ,soup.find_all("td")[::8])
port =map(lambda x:x.text ,soup.find_all("td")[1::8])
proxy = list(map(lambda x:x[0]+ ":" +x[1] , list(zip(ip,port))))
del proxy[len(proxy)-19:]
global proxy1
#print(proxy)

def proxies(proxy):
    try:
            global proxy1
            
            proxy1 = {"https": choice(proxy)}
            #print(proxy1)
            r = requests.get("https://www.google.com/" , proxies=proxy1,timeout=2)
            return 1
    except :
        
        return 0
	
def get_proxies():
    global proxy1
    
    while 1:
        k = proxies(proxy)
        if k :
            break
        else:
            continue
    return proxy1
    exit(0)


#q = get_proxies()
#print(q)
