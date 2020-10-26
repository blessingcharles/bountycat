import requests


headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language' : 'en-US,en;q=0.5',
            'Accept-Encoding' : 'gzip, deflate',
            'Upgrade-Insecure-Requests' : '1'}

def requester(url,GET=True,time=2):
    try:
        if GET:
            page = requests.get(url,timeout=time,headers=headers)
            return page
        if POST:
            page = requests.post(url,timeout=time)
            return page
    except:
        pass


        