import bs4
import requests

def get_html(url):
    r = requests.get(url)
    return r.text

