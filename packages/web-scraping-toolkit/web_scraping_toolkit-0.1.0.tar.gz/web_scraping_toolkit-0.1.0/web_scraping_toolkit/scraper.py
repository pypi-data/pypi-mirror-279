# scraper.py
import requests

class Scraper:
    def __init__(self, base_url, headers=None, proxies=None):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(headers or {})
        self.proxies = proxies

    def fetch_page(self, url):
        response = self.session.get(url, proxies=self.proxies)
        response.raise_for_status()
        return response.text

    def fetch_json(self, url):
        response = self.session.get(url, proxies=self.proxies)
        response.raise_for_status()
        return response.json()
