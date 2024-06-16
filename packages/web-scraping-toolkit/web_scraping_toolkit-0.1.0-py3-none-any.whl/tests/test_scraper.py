# tests/test_scraper.py
import unittest
from web_scraping_toolkit.scraper import Scraper

class TestScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper(base_url="https://example.com")

    def test_fetch_page(self):
        page_content = self.scraper.fetch_page("/test")
        self.assertIn("Example Domain", page_content)

if __name__ == '__main__':
    unittest.main()
