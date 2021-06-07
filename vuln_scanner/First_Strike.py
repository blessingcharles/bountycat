from requests.api import request
from templates.requester import requester
from templates.soup import soupObject
from templates.colors import *
from concurrent.futures import ThreadPoolExecutor

class FirstStrike :

    def __init__(self,url,timeout=10,hide_code=[],verbose=False):

        self.url = url
        self.timeout= timeout
        self.hide_code = hide_code
        self.verbose = verbose

    def hederParser(self,r):

        try:
            print(f"[+]{yellow}Server Running ----> {r.headers['Server']}{reset}")
        except:
            pass
        try:
            print("[+]X-Frame-Options --->",r.headers['X-Frame-Options'])
        except:
            print(f"{red}[-] CLICKJACKING ATTACK POSSIBLE DUE TO ABSENCE OF X-Frame-Options header{reset}")
        




    
    def scrap(self,path_scrapped_wordlist):

        
        r = requester(self.url,time=self.timeout)

        soup = soupObject(r.text)

        #finding the title
        title = soup.find('title').text
        print(f"{green}[+]TITLE OF THE WEBSITE{reset} ===> {yellow}{title}{reset}")
        words_in_page = ''.join(soup.stripped_strings)

        #parsing the header for useful info
        self.hederParser(r)

        black_list = ['/','*','&','-','=','+','%','|','(',')','[',']','{','}',',',';',':']

        #Scrap the main website to generate wordlist

        for b in black_list:
            words_in_page = words_in_page.replace(b," ")

        words = list(filter(lambda x: x != "",words_in_page.split()))

        with open(path_scrapped_wordlist,'a') as f:
            for word in words:
                f.write(word+'\n')

        print(f"{green}[+]SCRAPPED ALL WORDS AND DETAILS FROM THE MAIN WEBPAGE PRINTED {reset}====> {yellow}{path_scrapped_wordlist}{reset}")
        print(f"{green}[+]TOTAL GENERATED WORDS FROM THE MAIN WEBPAGE{reset} ===>{yellow} {len(words)}{reset}")

    def hit(self,directory):

        r = requester(f"{self.url}/{directory}")
        if r.status_code < 400 :
            print(f"{blue}SENSITIVE FILES RESPONSE CODE[{r.status_code}]{reset}----->{yellow} {self.url}/{directory}{reset}")


    def Site_lookup(self,url):
        req_url = url
        directories = ['xmlrpc.php','admin','Admin','robots.txt','phpmyadmin','robots','sitemap.xml','Sitemap','sitemap']

        print(f"{green} [### {url} ###] {reset}                                     ")

        # with ThreadPoolExecutor(max_workers=10) as executor:
        #     executor.map(self.hit,directories)
        for directory in directories:
            
            try:
                if self.verbose :print(f"trying  {req_url}/{directory}                                                          ",end="\r",flush=True)

                r = requester(f"{req_url}/{directory}",time=self.timeout)

                if r.status_code in self.hide_code: pass
                elif r.status_code < 400 :
                    print(f"{red}SENSITIVE FILES RESPONSE CODE[{r.status_code}]{reset}----->{yellow} {req_url}/{directory}{reset}")
            
            except:
                pass
         
            
           


