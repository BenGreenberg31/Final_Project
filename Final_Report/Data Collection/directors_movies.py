import imdb_scraper
import sys
import os
import json
import re
import pandas as pd

def scraping_full_credits(director_ids):
    for id in director_ids:
        credits_dictionary = imdb_scraper.get_full_credits_for_director(id)
        directory = id
        if not os.path.exists(directory):
            os.makedirs(directory)
            json_file_path = os.path.join(directory, '{}.json'.format(id))
            with open(json_file_path, 'w') as json_file:
                json.dump(credits_dictionary, json_file)

def read_json_files_from_directory(directory):
    json_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                json_data.append(data)
    return json_data

def create_csv(directories):
    all_json_data = []
# Loop through each directory and read JSON files
    all_credits = []
    for directory in director_ids:
        try:
            json_data = read_json_files_from_directory(directory)
            all_json_data.extend(json_data)
            for entry in json_data:
                director_name = entry.get("director_name", "")
                credits = entry.get("credits", [])
    
    # Extract credits
            for credit in credits:
                credit["director_name"] = director_name
                credit["director_id"] = directory
                all_credits.append(credit)
        except FileNotFoundError:
            print("Directory not found:", directory)

if __name__ == '__main__':
    csv_file = sys.argv[0]
    df = pd.read_csv(csv_file)

    urls = df['IMDb_URI'].to_list()

    director_ids = []
    for url in urls:
        pattern = r'(nm\d+)/'
# Using re.search to find the pattern in the URL
        match = re.search(pattern, url)
        if match:
            extracted_string = match.group(1)
            director_ids.append(extracted_string)
        else:
            print("Pattern not found in the URL.")

    