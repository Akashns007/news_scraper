import os
import json
import subprocess

def run_spider():
    output_file = "latest_news.json"
    
    # Read existing news data if the file exists
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            existing_news = json.load(file)
    else:
        existing_news = []

    # Run the spider in a separate process to avoid ReactorNotRestartable error
    subprocess.run(["scrapy", "runspider", "news.py", "-o", "temp_latest_news.json", "-t", "json"])

    # Load the new data
    with open("temp_latest_news.json", 'r') as file:
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
    os.remove("temp_latest_news.json")
