# setup.py
from setuptools import setup, find_packages

setup(
    name="web_scraping_toolkit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "web_scraper=web_scraping_toolkit.scraper:main",
        ],
    },
    author="Vijeth21",
    author_email="vijethfernandes21@gmail.com",
    description="A toolkit for web scraping",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/21Vijeth/web_scraping_toolkit.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
