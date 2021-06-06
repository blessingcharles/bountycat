from bs4 import BeautifulSoup

def soupObject(html_content):

    return BeautifulSoup(html_content,'html.parser')