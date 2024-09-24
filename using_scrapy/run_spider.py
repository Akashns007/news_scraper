import os
import json
import subprocess

def run_spider():
    output_file = "latest_news.json"
    temp_file = "temp_latest_news.json"

    # Read existing news data if the file exists
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            existing_news = json.load(file)
    else:
        existing_news = []

    # Run the spider in a separate process
    result = subprocess.run(["scrapy", "crawl", "news", "-o", temp_file, "-t", "json"], capture_output=True, text=True)

    # Log any errors if Scrapy fails
    if result.returncode != 0:
        print("Error running Scrapy:", result.stderr)
        return

    # Check if the temp file exists
    if not os.path.exists(temp_file):
        print("Error: Temp file not created.")
        return

    # Load the new data from the temporary file
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
