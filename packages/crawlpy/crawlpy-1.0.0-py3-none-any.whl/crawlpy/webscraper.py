import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

class WebScraper:
    def __init__(self, headers=None, timeout=10, retries=3, backoff_factor=0.3, max_workers=5, use_selenium=False):
        self.session = requests.Session()
        self.timeout = timeout
        self.max_workers = max_workers
        self.use_selenium = use_selenium

        if headers is None:
            headers = {}
        self.session.headers.update(headers)
        
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def fetch_url(self, url):
        try:
            print(f"Starting to scrape {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            print(f"Finished scraping {url}")
            return response.text
        except requests.RequestException as e:
            print(f"An error occurred while scraping {url}: {e}")
            return f"An error occurred: {e}"

    def fetch_url_with_selenium(self, url):
        try:
            print(f"Starting to scrape {url} with Selenium")
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # To run Chrome in headless mode
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            page_source = driver.page_source
            driver.quit()
            print(f"Finished scraping {url} with Selenium")
            return page_source
        except WebDriverException as e:
            print(f"Selenium error occurred while scraping {url}: {e}")
            return f"An error occurred: {e}"

    def get_page_text(self, urls):
        if isinstance(urls, str):
            urls = [urls]
        texts = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {
                executor.submit(self.fetch_url_with_selenium if self.use_selenium else self.fetch_url, url): url
                for url in urls
            }
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    response_text = future.result()
                    soup = BeautifulSoup(response_text, 'html.parser')
                    texts.append(soup.get_text())
                except Exception as e:
                    print(f"An error occurred while processing {url}: {e}")
                    texts.append(f"An error occurred: {e}")

        return texts if len(texts) > 1 else texts[0]

    def save_to_file(self, urls, filename, file_type='txt', column_names=None):
        text = self.get_page_text(urls)
        print(f"Saving scraped content to {filename} as {file_type}")
        if file_type == 'txt':
            with open(filename, 'w', encoding='utf-8') as file:
                if isinstance(text, list):
                    for page_text in text:
                        file.write(page_text + "\n\n")
                else:
                    file.write(text)
        elif file_type == 'json':
            with open(filename, 'w', encoding='utf-8') as file:
                if isinstance(text, list):
                    json.dump(text, file, ensure_ascii=False, indent=4)
                else:
                    json.dump([text], file, ensure_ascii=False, indent=4)
        elif file_type == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if column_names:
                    writer.writerow(column_names)
                if isinstance(text, list):
                    for page_text in text:
                        writer.writerow([page_text])
                else:
                    writer.writerow([text])
        print(f"Saved content to {filename}")
        return f"Saved content to {filename}"

    def get_tag_content(self, url, tag_name):
        try:
            page_source = self.fetch_url_with_selenium(url) if self.use_selenium else self.fetch_url(url)
            print(f"Scraping tags <{tag_name}> from {url}")
            soup = BeautifulSoup(page_source, 'html.parser')
            tags = soup.find_all(tag_name)
            print(f"Finished scraping tags <{tag_name}> from {url}")
            return [tag.get_text() for tag in tags]
        except Exception as e:
            print(f"An error occurred while scraping tags <{tag_name}> from {url}: {e}")
            return f"An error occurred: {e}"

    def extract_links(self, url):
        try:
            page_source = self.fetch_url_with_selenium(url) if self.use_selenium else self.fetch_url(url)
            print(f"Extracting links from {url}")
            soup = BeautifulSoup(page_source, 'html.parser')
            links = soup.find_all('a', href=True)
            print(f"Finished extracting links from {url}")
            return [link['href'] for link in links]
        except Exception as e:
            print(f"An error occurred while extracting links from {url}: {e}")
            return f"An error occurred: {e}"
        
    def take_screenshot(self, url, filename="screenshot.png"):
        try:
            print(f"Taking screenshot of {url}")
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            driver.save_screenshot(filename)
            driver.quit()
            print(f"Screenshot saved as {filename}")
            return filename
        except WebDriverException as e:
            print(f"Selenium error occurred while taking screenshot of {url}: {e}")
            return None

# Exporting the class from the module
__all__ = ['WebScraper']