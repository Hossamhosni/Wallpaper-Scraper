import unittest
import scraper
import requests
from bs4 import BeautifulSoup

class TestScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        TestScraper.url = 'https://wall.alphacoders.com/search.php?search=batman+joker'
        response = requests.get(TestScraper.url)
        TestScraper.soup = BeautifulSoup(response.text, 'html.parser')

    def test_get_page_url(self):
        result = scraper.get_page_url('batman joker')
        self.assertEqual(
            TestScraper.url, result)

    def test_get_page_url2(self):
        result = scraper.get_page_url('bioshock')
        self.assertEqual('https://wall.alphacoders.com/search.php?search=bioshock', result)

    def test_get_container_divs(self):
        result = scraper.get_containing_divs(TestScraper.soup)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result[0]['id'])

    def test_get_pages_url_based_on_number_of_images(self):
        result = scraper.get_pages_url_based_on_number_of_images(TestScraper.url, 100)
        self.assertEqual(result[0], TestScraper.url)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1], TestScraper.url + "&page=2")

if __name__ == '__main__':
    unittest.main()
