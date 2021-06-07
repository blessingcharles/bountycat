import argparse

from templates.banner import banner , print_line
from templates.colors import *
from templates.create_directory import dir_create

from bounty_cat import Scanner


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
    parser.add_argument("--timeout",dest="timeout",type=int,help="enter the timeout for each requests [default 10 seconds]",default=10)
    parser.add_argument("-o","--output",dest="output",help="enter the directory name to store the outputs",default="Bounty")
    parser.add_argument("-cp","--change-ip",dest="ip_proxy",help="change ip to get rid of ip blocks [may get some false negatives]",default=False)
    parser.add_argument("-d","--depth",dest="depth",help="depth to scrap [default 5] otherwise it may loop forever",default=5,type=int)
    parser.add_argument("-ctf",help="set this flag to scan for ctf games",action="store_true")
    parser.add_argument("-w","--wordlist",dest="wordlist",help="default set to jshaddix all.txt")
    parser.add_argument("-hc","--hide-code",dest="hide_code",help="enter the response codes comma separated to hide while bruteforcing")
    parser.add_argument("--port",type=int,default=443,dest="port",help="set -port 80 for http website [default https port 443]")
    parser.add_argument("-v","--verbose",action="store_true",default=False,dest="verbose",help="set for verbose output")

    
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
    port = parser.port
    hide_code = parser.hide_code
    verbose = parser.verbose
    
    if hide_code is not None : hide_code = list(map( lambda x : int(x), hide_code.split(",") ))
    else : hide_code = []

    if  not url and not urls_file:
        print(f"{red}ENTER A VALID INPUT [URL OR URLS CONTAINING FILE] \n TRY python3 start.py --help{reset}")
        quit()

    
    fullpath = dir_create(output_file)

    if wordlist:

        print("wordlist provided "+ wordlist)

        try:
            with open(wordlist,'r') as f:
                pass

            scanner = Scanner(url,port,threads,timeout,fullpath,depth,hide_code,wordlist,verbose=verbose)

        except:
            print("failed to open wordlist")
            exit()


    else :
        scanner = Scanner(url,port,threads,timeout,fullpath,depth,hide_code,wordlist="Payloads/All.txt",verbose=verbose)

    scanner.start()
