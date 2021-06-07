from urllib.request import urlparse


from templates.banner import  print_line

from templates.colors import *
from templates.create_directory import dir_create
from templates.requester import requester
import templates.HandleSignals

from Addons.screen_capture import Screenshots

from vuln_scanner.First_Strike import FirstStrike
from vuln_scanner.Ping import Ping_the_host
from vuln_scanner.brute_directories import Brute
from vuln_scanner.dns_records import SPF
from vuln_scanner.linksscrapper import get_all_url_waybackmachine , get_all_tag_links , get_all_urls_with_params
from vuln_scanner.Subdomain_enum import Sub_Enum
from vuln_scanner.Open_redirect import get_all_urls_with_redirection



class Scanner:

    def __init__(self,url,port,threads,timeout,output_file_path,depth,hide_code,wordlist,ctf=False,verbose=False):

        self.url = url
        self.threads = threads
        self.timeout =timeout
        self.domain = urlparse(self.url).netloc
        self.fullpath = output_file_path
        self.depth = depth
        self.ctf = ctf
        self.wordlist = wordlist
        self.hide_code = hide_code
        self.port = port
        self.verbose = verbose

        #storing the results path

        self.waybackurl = f"{self.fullpath}/waybackurls.txt"
        self.anchor_path = f"{self.fullpath}/anchor_links.txt"
        self.script_path = f"{self.fullpath}/script_links.txt"
        self.subdomain_path = f"{self.fullpath}/subdomains.txt"
        self.scrapped_wordlist = f"{self.fullpath}/scrapped_wordlist_from_mainwebpage.txt"

    def start(self):

        #pinging
        Ping_the_host(self.domain)
        print_line(blue,reset)

        #inital Strike
        scrap = FirstStrike(self.url , self.timeout,self.hide_code)
        scrap.scrap(self.scrapped_wordlist)
        print_line(green,reset)

        #domain vuln checking
        SPF(self.domain)
        print_line(green,reset)

        print(f'{blue} SUBDOMAIN ENUMERATION {reset}')
        #subdomain enumeration

        subd = Sub_Enum(self.domain,self.subdomain_path)
        subd.crtsh_subdomain_enum()
        subd.iterate_through_wildcards()
        print_line(green,reset)
        
        #Sensitive files
        print(f'{blue} SENSITIVE FILES ENUMERATION {reset}')
        scrap = FirstStrike("",self.timeout,self.hide_code,self.verbose)
        with open(self.subdomain_path,'r') as domains:
            for domain in domains:
                #print(domain)
                scrap.Site_lookup(f"https://{domain.strip()}")

        print_line(green,reset)

        #url scrapping

        print(f'{blue} URL SCRAPPING {reset}')
        get_all_url_waybackmachine(self.domain,self.waybackurl)

        get_all_tag_links(self.url,self.anchor_path,self.depth,"a")

        get_all_tag_links(self.url,self.script_path,self.depth,"script")
        print_line(green,reset)

        #parsing the scrapped urls
        print(f'{blue} URL PARSING{reset}')
        get_all_urls_with_params(f'{self.fullpath}/anchor_links.txt',self.fullpath)
        get_all_urls_with_params(f'{self.fullpath}/waybackurls.txt',self.fullpath)

        print_line(green,reset)

        #taking screenshots
        print(f"{blue}SCREEN SHOTTING ALL SUBDOMAINS{reset}")
        self.Screen_shot()
        print_line(green,reset)


        #checking for possible open redirection
        get_all_urls_with_redirection('Bounty/params_urls.txt','Bounty/redirect_params.txt','Payloads/redirects_params.txt')
        print_line(green,reset)


        #finding sub directories in the domains
        print(f"{blue}BRUTEFORCING DIRECTORIES IN SUBDOMAIN{reset}")
        self.dirbrute()
        print_line(green,reset)

    def Screen_shot(self):
    
        Screen_shot_directory = dir_create(f'{self.fullpath}/Screenshots')

        snap = Screenshots(Screen_shot_directory)

        with open(self.subdomain_path,'r') as domains:

            for domain in domains:
                snap.capture(domain.strip())

        print(f"ScreenShots saved ------> {self.fullpath}/Screeshots")

        snap.end


    def dirbrute(self):

        try:
            with open(self.subdomain_path,'r') as domains:
                for domain in domains:
                    domain = domain.strip()
                    r = requester(f"https://{domain}",time=self.timeout)

                    if r.status_code in self.hide_code: pass
                    elif r.status_code < 400:
                        print(f"BRUTEFORCING DIRECTORIES IN {domain}")
                        Brute(domain,"Bounty",self.wordlist).dir_brute()

        except:
            pass
