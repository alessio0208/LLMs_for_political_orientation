import requests
from bs4 import BeautifulSoup
import json
import os
import csv
from datetime import datetime

# Define root and directory paths
ROOT = 'output'
OUTPUT_DIR = os.path.join(ROOT, 'urls')
FAILURE_DIR = os.path.join(ROOT, 'errors')

class UrlExtractor:
    """
    A class to extract article URLs from a newspaper website and save them to a JSON file.
    """

    def fetch_article_urls(self, newspaper_url):
        """
        Fetches article URLs from a given newspaper website URL.
        
        Parameters:
        newspaper_url (str): The URL of the newspaper website.
        
        Returns:
        list: A list of unique article URLs.
        """
        # Send a request to the newspaper URL
        response = requests.get(newspaper_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all anchor tags, assuming that articles are in <a> tags with href attributes
        links = soup.find_all('a', href=True)
        
        # Filter and collect up to 200 unique article URLs
        article_urls = []
        for link in links:
            url = link['href']
            if url.startswith('http'):  # Simple filter to get absolute URLs
                if url not in article_urls:
                    article_urls.append(url)
                    if len(article_urls) == 200:
                        break
        
        return article_urls

    def save_urls_to_json(self, newspaper_url, article_urls):
        """
        Saves the collected article URLs to a JSON file.
        
        Parameters:
        newspaper_url (str): The URL of the newspaper website.
        article_urls (list): A list of article URLs.
        """
        current_date = datetime.now()
        date_string = current_date.strftime('%Y-%m-%d')
        
        file_path = os.path.join(OUTPUT_DIR, f'{date_string}_urls.json')
        
        # Check if file exists and read existing data
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
        else:
            data = {}

        # Update data with new URLs ensuring no duplication
        if newspaper_url in data:
            # Create a set of existing URLs and update with new ones
            existing_urls = set(data[newspaper_url])
            updated_urls = existing_urls.union(set(article_urls))
            data[newspaper_url] = list(updated_urls)
        else:
            data[newspaper_url] = article_urls

        # Write updated JSON data to the file
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def log_faulty_url(self, url):
        """
        Logs a faulty URL to a CSV file.
        
        Parameters:
        url (str): The faulty URL to be logged.
        """
        os.makedirs(FAILURE_DIR, exist_ok=True)
        with open(os.path.join(FAILURE_DIR, 'faulty_urls.csv'), 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([url])
