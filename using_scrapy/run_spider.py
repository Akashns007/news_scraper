import os
import json
import subprocess

def run_spider():
    # Define paths for the output and temporary files
    output_file = os.path.join(os.path.dirname(__file__), "latest_news.json")
    temp_file = os.path.join(os.path.dirname(__file__), "temp_latest_news.json")
    
    # Read existing news data if the output file exists
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            existing_news = json.load(file)
    else:
        existing_news = []

    # Run the spider in a separate process to avoid ReactorNotRestartable error
    try:
        subprocess.run(["scrapy", "crawl", "news", "-o", "temp_latest_news.json", "-t", "json"])
    except subprocess.CalledProcessError as e:
        print(f"Error running Scrapy spider: {e}")
        return  # Exit the function if the spider fails

    # Load the new data from the temporary file
    try:
        with open(temp_file, 'r') as file:
            new_news = json.load(file)
    except FileNotFoundError:
        print(f"Temporary file '{temp_file}' not found.")
        return  # Exit the function if the temporary file is missing
    except json.JSONDecodeError:
        print(f"Error decoding JSON from '{temp_file}'.")
        return  # Exit if the JSON data is invalid

    # Filter out duplicates
    existing_links = {news['news_link'] for news in existing_news}
    unique_news = [news for news in new_news if news['news_link'] not in existing_links]

    # Append new unique news to existing news
    updated_news = existing_news + unique_news

    # Save the updated news to the output file
    with open(output_file, 'w') as file:
        json.dump(updated_news, file, indent=4)

    # Remove the temporary file if it exists
    if os.path.exists(temp_file):
        os.remove(temp_file)
