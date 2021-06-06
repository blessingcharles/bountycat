from bs4 import BeautifulSoup
from urllib.request import urlparse , urljoin
from templates import requester

global internal_urls
internal_urls = []
global junk_extensions
junk_extensions = ['.jpeg','.png','.jpg','.pdf','.docs']


def link_scrapper(url,domain_name,link_tag,attribute,fd):
    try:
        r = requester.requester(url)
        soup = BeautifulSoup(r.content,"html.parser")

        for a_tags in soup.findAll(link_tag):
            href = a_tags.attrs.get(attribute)
            href = urljoin(url,href)

            if domain_name not in href or href in internal_urls:
                continue
            fd.write(href+'\n')
            if not href.endswith(tuple(junk_extensions)):
                internal_urls.append(href)

    except:
        pass

   



def get_all_tag_links(url,path,depth,link_tag):
    
    domain_name = urlparse(url).netloc

    if link_tag == 'a':
        attribute = 'href'

        count = 0

        with open(path,'a') as fd:
            link_scrapper(url,domain_name,link_tag,attribute,fd)
            for url in internal_urls:
                link_scrapper(url,domain_name,link_tag,attribute,fd)
                count = count+1

                if(count == depth):
                    break

            print(f"SCRAPPED URLS PRINTED TO ------> {path}")

    
    if link_tag == 'script':
        attribute = 'src'

        count = 0

        with open(path,'a') as fd:
            link_scrapper(url,domain_name,link_tag,attribute,fd)
            for url in internal_urls:
                link_scrapper(url,domain_name,link_tag,attribute,fd)
                count = count+1
                if count == depth :
                    break

            print(f"SCRAPPED JS URLS PRINTED TO ------> {path}")

# way back url
def get_all_url_waybackmachine(domain,path):

    waybackurl = 'http://web.archive.org/cdx/search/cdx?url=*.%s/*&output=text&fl=original&collapse=urlkey'%domain
    r = requester.requester(waybackurl,time=10)

    urls = r.text
    
    with open(path , 'a') as f:
        for url in urls:
            f.write(url)

    print(f"WAYBACK URLS PRINTED TO ------> {path}")

#get_all_url_waybackmachine("annauniv.edu","urls.txt")


def get_all_urls_with_params(search_file_path,params_path_name):

    with open(params_path_name+'/params_urls.txt','a') as fd1:

        with open(search_file_path,'r') as fd2:

            for url in fd2:
                flag = bool(urlparse(url).query)
                
                if flag:
                    fd1.write(url)
            
    print(f"SCRAPPED URLS WITH PARAMS PRINTED TO ------> {params_path_name}/params_urls.txt ")


def get_all_urls_with_redirection(search_file_path,params_path_name,path_payloads):

        redir_params_url = []
        payloads = []

        with open(path_payloads,'r') as fd2:
            for payload in fd2:
                payloads.append(payload.strip())

        with open(search_file_path,'r') as fd1:        
            redir_params_url = [url for url in fd1 for payload in payloads if payload in url]

            
        with open(params_path_name,'a') as fd1:
            
            for url in redir_params_url:
                fd1.write(url)
         



    
    
