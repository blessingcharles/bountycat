from urllib.request import urlparse
import argparse
import time


from templates.banner import banner , print_line
from templates.headers import headers
from templates.colors import *
from templates.create_directory import dir_create
from templates.requester import requester

from Addons.screen_capture import Screenshots

from vuln_scanner.brute_directories import Brute
from vuln_scanner.dns_records import SPF
from vuln_scanner.linksscrapper import get_all_url_waybackmachine , get_all_tag_links , get_all_urls_with_params
from vuln_scanner.Subdomain_enum import Sub_Enum
import os


class Scanner:

    def __init__(self,url,threads,timeout,output_file_path,depth,hide_code,wordlist,ctf=False):

        self.url = url
        self.threads = threads
        self.timeout =timeout
        self.domain = urlparse(self.url).netloc
        self.fullpath = output_file_path
        self.depth = depth
        self.ctf = ctf
        self.wordlist = wordlist
        self.hide_code = hide_code

        self.waybackurl = f"{self.fullpath}/waybackurls.txt"
        self.anchor_path = f"{self.fullpath}/anchor_links.txt"
        self.script_path = f"{self.fullpath}/script_links.txt"
        self.subdomain_path = f"{self.fullpath}/subdomains.txt"

    def start(self):

        #domain vuln checking

        SPF(self.domain)
        print_line(green,reset)

        print(f'{blue} SUBDOMAIN ENUMERATION {reset}')
        #subdomain enumeration

        subd = Sub_Enum(self.domain,self.subdomain_path)
        subd.crtsh_subdomain_enum()
        subd.iterate_through_wildcards()
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
                    r = requester(f"https://{domain}",time=10)
                    if r.status_code < 400:
                        print(f"BRUTEFORCING DIRECTORIES IN {domain}")
                        Brute(domain,"Bounty",self.wordlist).dir_brute()

        except:
            pass

if __name__ == "__main__":

    print_line(red,reset)
    banner(blue,reset)
    print_line(red,reset)
    parser = argparse.ArgumentParser(description="bounty cat")

    parser.add_argument("-u","--url",dest="url",help="enter a valid url")
    parser.add_argument("-f","--file",dest="files",help="enter a file containing urls")
    parser.add_argument("-H" ,"--headers",dest="headers",help="enter headers")
    parser.add_argument("-t","--threads",dest="threads",type=int,default=3,help="enter the number of threads [default 3]")
    parser.add_argument("-p","--proxy",dest="proxy",help="enter a proxy [ip:port]")
    parser.add_argument("--timeout",dest="timeout",type=int,help="enter the timeout for each requests [default 2 seconds]",default=2)
    parser.add_argument("-o","--output",dest="output",help="enter the directory name to store the outputs",default="Bounty")
    parser.add_argument("-cp","--change-ip",dest="ip_proxy",help="change ip to get rid of ip blocks [may get some false negatives]",default=False)
    parser.add_argument("-d","--depth",dest="depth",help="depth to scrap [default 5] otherwise it may loop forever",default=5,type=int)
    parser.add_argument("-ctf","--capture-the-flag",dest='ctf',default=False,type=bool,help="set this flag to scan for ctf games")
    parser.add_argument("-w","--wordlist",dest="wordlist",help="default set to jshaddix all.txt")
    parser.add_argument("-hc","--hide-code",dest="hide_code",help="enter the response codes comma separated to hide while bruteforcing")
    parser = parser.parse_args()
    
    url = parser.url
    urls_file = parser.files
    headers = parser.headers
    threads = parser.threads
    proxy = parser.proxy
    timeout = parser.timeout
    output_file = parser.output
    change_ip = parser.ip_proxy
    depth = parser.depth
    ctf = parser.ctf
    wordlist = parser.wordlist
    hide_code = parser.hide_code

    if  not url and not urls_file:
        print(f"{red}ENTER A VALID INPUT [URL OR URLS CONTAINING FILE] \n TRY python3 bounty_cat.py --help{reset}")
        quit()

    
    fullpath = dir_create(output_file)

    if wordlist:
        print("wordlist provided "+ wordlist)
        with open(wordlist,'r') as f:
            pass
        scanner = Scanner(url,threads,timeout,fullpath,depth,hide_code,wordlist)
    else :
        scanner = Scanner(url,threads,timeout,fullpath,depth,hide_code,wordlist="Payloads/All.txt")

    scanner.start()
