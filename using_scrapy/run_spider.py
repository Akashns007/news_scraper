import os
import json
import subprocess

def run_spider():
    output_file = "latest_news.json"
    
    # Read existing news data if the file exists
    existing_news = []
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r') as file:
                existing_news = json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading {output_file}: {e}")

    # Run the spider in a separate process
    result = subprocess.run(["scrapy", "runspider", "news.py", "-o", "temp_latest_news.json", "-t", "json"], capture_output=True, text=True)

    # Check if the spider ran successfully
    if result.returncode != 0:
        print(f"Error running Scrapy: {result.stderr}")
        return  # Stop execution if the spider fails

    # Check if the output file was created
    if not os.path.exists("temp_latest_news.json"):
        print("Error: temp_latest_news.json not found after running Scrapy.")
        return

    # Load the new data
    try:
        with open("temp_latest_news.json", 'r') as file:
            new_news = json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading temp_latest_news.json: {e}")
        return

    # Filter out duplicates
    existing_links = {news['news_link'] for news in existing_news}
    unique_news = [news for news in new_news if news['news_link'] not in existing_links]

    # Append new unique news to existing news
    updated_news = existing_news + unique_news

    # Save the updated news to the output file
    try:
        with open(output_file, 'w') as file:
            json.dump(updated_news, file, indent=4)
    except IOError as e:
        print(f"Error writing to {output_file}: {e}")

    # Remove the temporary file
    os.remove("temp_latest_news.json")
