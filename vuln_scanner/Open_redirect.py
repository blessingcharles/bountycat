import re
from templates.requester import requester
from templates.colors import *
from concurrent.futures import ThreadPoolExecutor

def Find_redirect(url):
    
    flag = 'bing'
    print(f"{yellow}[+] CHECKING FOR  OPENREDIRECTION  -----> {reset}{url}                                      ",end='\r',flush=True)
    
    r = requester(url)
    if r.status_code == 200:
        if flag in r.text:
            print(f"{red}[-]OPEN REDIRECTION MAY POSSIBLE -->", url)


def get_all_urls_with_redirection(search_file_path,params_path_name,path_payloads):

        redir_params_url = []
        payloads = []
        REDIRECT_SITE = "https://www.bing.com"

        #opening the file containg open redirects payload
        with open(path_payloads,'r') as fd2:
            for payload in fd2:
                payloads.append(payload.strip())

        #opening file containg urls with params
        with open(search_file_path,'r') as fd1:        
            for url in fd1:
                for payload in payloads:
                    if payload in url:

                        regex1 = payload+r".*[^&]"
                        replace = payload+REDIRECT_SITE

                        url = re.sub(regex1,replace,url.strip(),flags=re.I)
                        if url not in redir_params_url:
                            redir_params_url.append(url)

        #Appending the redirect url with changing the param with regex to REDIECT SITE

        with open(params_path_name,'a') as fd1:                            
            for url in redir_params_url:
                    fd1.write(url+'\n')

        print(f"[+]POSSIBLE OPEN REDIRECT URLS PRINTED TO {params_path_name}")

        #scanning every url for open redirection
        print(f"{blue} [ CHECKING FOR OPEN REDIRECTION ] {reset}")
        with ThreadPoolExecutor(max_workers=10) as executor:

            executor.map(Find_redirect,redir_params_url)

               