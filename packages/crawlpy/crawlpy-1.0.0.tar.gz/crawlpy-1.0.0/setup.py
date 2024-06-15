from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crawlpy",
    version="1.0.0",
    author="Pranav Kumar",
    author_email="pranavkumarnair@gmail.com",
    description="A Python package for web scraping and YouTube video scraping",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PraNavKumAr01/pyscrapy",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "pytube",
        "deepgram-sdk",
        "httpx",
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)