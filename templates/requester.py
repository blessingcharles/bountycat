import requests

from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language' : 'en-US,en;q=0.5',
            'Accept-Encoding' : 'gzip, deflate',
            'Upgrade-Insecure-Requests' : '1'}

def requester(url,GET=True,POST=False,time=10):
    try:
        if GET:
            page = requests.get(url,headers=headers , timeout=time)
          #  print(page)
            return page
        if POST:
            page = requests.post(url)
            return page
    except:
        pass



        