import re
import requests
from bs4 import BeautifulSoup

def get_html(url):
    res = requests.get(url)
    return res.text

def get_terms(html):
    soup = BeautifulSoup(html, 'html.parser')

    options = [o.text for o in soup.find('select', id='ddlTerm').find_all('option') if o.text != '---------------']
    
    results = [tuple(map(int, re.findall(r'\d+', o))) for o in options]
    return results