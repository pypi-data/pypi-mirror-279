
import unittest
from crawlpy import WebScraper

class TestWebScraper(unittest.TestCase):
    def test_get_page_text_single(self):
        url = "https://google.com"
        result = WebScraper.get_page_text(url)
        self.assertTrue(isinstance(result, str))

    def test_get_page_text_multiple(self):
        urls = ["https://google.com", "https://wikipedia.org"]
        result = WebScraper.get_page_text(urls)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 2)

    def test_save_to_file(self):
        url = "https://google.com"
        filename = "test_output.txt"
        result = WebScraper.save_to_file(url, filename)
        self.assertTrue(result.endswith(f"Saved content to {filename}"))

    def test_get_tag_content(self):
        url = "https://google.com"
        result = WebScraper.get_tag_content(url, "h1")
        self.assertTrue(isinstance(result, list))

if __name__ == "__main__":
    unittest.main()