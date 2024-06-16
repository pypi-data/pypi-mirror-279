# CrawlPY

CrawlPY is a Python package for web scraping and YouTube video scraping.

## Features

- **Web Scraping**: Easily scrape web pages using requests and BeautifulSoup.
- **YouTube Scraping**: Scrape YouTube videos and download them.
- **Audio Transcription**: Transcribe audio from videos using Deepgram API.
- **Selenium Support**: Support for websites that require JavaScript rendering.

## Installation

You can install CrawlPY using pip:

```bash
pip install crawlpy
```

# Web Scraper
## Initializing the WebScraper

## To start using the `WebScraper`, you need to create an instance of it. You can customize headers, timeout, retries, and other settings.

```python
from pyscrapy import WebScraper

scraper = WebScraper(headers={'User-Agent': 'Mozilla/5.0'}, timeout=15, retries=5, use_selenium=False)
```

# Fetching Page Text
## You can fetch the text content of a single URL or multiple URLs. The function returns the plain text content of the web pages.

```python
# Single URL
text = scraper.get_page_text("https://google.com")
print(text)

# Multiple URLs
texts = scraper.get_page_text(["https://google.com", "https://wikipedia.com"])
for text in texts:
    print(text)
```

# Saving Scraped Content to a File
## You can save the scraped content to a file in different formats: txt, json, or csv. You can also provide column names for the CSV format.

```python
# Save as plain text
scraper.save_to_file("https://google.com", "output.txt", file_type='txt')

# Save as JSON
scraper.save_to_file(["https://google.com", "https://wikipedia.com"], "output.json", file_type='json')

# Save as CSV with column names
scraper.save_to_file(["https://google.com", "https://wikipedia.com"], "output.csv", file_type='csv', column_names=['Content'])
```

# Extracting Specific HTML Tags
## You can extract content from specific HTML tags. The function returns the text content of all occurrences of the specified tag.

```python
tags_content = scraper.get_tag_content("https://google.com", "p")
for content in tags_content:
    print(content)
```

# Extracting Links
## You can extract all the links (`<a>` tags) from a web page.

```python
links = scraper.extract_links("https://example.com")
for link in links:
    print(link)
```

# Taking Screenshots
## You can take a screenshot of a web page and save it as an image file. This feature uses Selenium.

```python
screenshot_file = scraper.take_screenshot("https://google.com", filename="screenshot.png")
```

# Using Selenium for JavaScript-Heavy Websites
## If you need to scrape content from websites that require JavaScript rendering, enable Selenium when initializing the WebScraper.

```python
scraper = WebScraper(use_selenium=True)

# Now all scraping functions will use Selenium
text = scraper.get_page_text("https://example.com")
print(text)
```

# YouTube Scraper
## The YouTube scraper in CrawlPy allows you to download YouTube videos and transcribe their audio content using the Deepgram API. To use this functionality, ensure you have set up your environment with the required API keys.

# Prerequisites
## Install Dependencies:

```python
pip install crawlpy
```

# Set Up Environment Variables:
## You need to set up your Deepgram API key as an environment variable. Create a .env file in your project directory and add your API key:

```env
DEEPGRAM_API_KEY=your_deepgram_api_key
```

## or add an environment variable into your code space

```python
import os

os.environ["DEEPGRAM_API_KEY"] = deepgram_api_key
```

# Initializing the YouTube Scraper
## To use the YouTube scraper, you need to create an instance of the YouTubeScraper class.

```python
from crawlpy import YouTubeScraper

youtube_scraper = YouTubeScraper()
```

# Downloading YouTube Videos
## You can download a YouTube video by providing its URL.

```python
video_url = "https://www.youtube.com/watch?v=oHg5SJYRHA0"
file_path = youtube_scraper.download_video(video_url)
print(f"Video downloaded to {file_path}")
```

# Transcribing YouTube Videos
## You can transcribe the audio content of a YouTube video. The transcriber function can take either a URL or the path to a previously downloaded video file.

```python
# Transcribe using a video URL
transcript = youtube_scraper.transcribe_video(video_url)
print("Transcript:", transcript)

# Optionally, save the transcript to a file
transcript = youtube_scraper.transcribe_video(video_url, save=True, filename="transcript.txt")
print(f"Transcript saved to {transcript}")
```

# License
## This project is licensed under the MIT License - see the LICENSE file for details.