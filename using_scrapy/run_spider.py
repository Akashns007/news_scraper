import os
import json
import subprocess

def run_spider():
    output_file = os.path.join(os.path.dirname(__file__), "latest_news.json")
    temp_file = os.path.join(os.path.dirname(__file__), "temp_latest_news.json")
    
    # Read existing news data if the file exists
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            existing_news = json.load(file)
    else:
        existing_news = []

    # Run the spider using the crawl command (ensure news.py is in spiders folder)
    subprocess.run(["scrapy", "crawl", "news", "-o", temp_file, "-t", "json"])

    # Load the new data
    with open(temp_file, 'r') as file:
        new_news = json.load(file)

    # Filter out duplicates
    existing_links = {news['news_link'] for news in existing_news}
    unique_news = [news for news in new_news if news['news_link'] not in existing_links]

    # Append new unique news to existing news
    updated_news = existing_news + unique_news

    # Save the updated news to the output file
    with open(output_file, 'w') as file:
        json.dump(updated_news, file, indent=4)

    # Remove the temporary file
    os.remove(temp_file)
