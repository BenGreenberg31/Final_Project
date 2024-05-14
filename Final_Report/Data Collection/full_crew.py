import imdb_scraper
import sys
import os
import json
import re
import pandas as pd
import csv

def movies_json(director_ids, df):
    for id in director_ids:
        subset_director_movies = df.loc[df['director_id'] == id]
        movies_list = subset_director_movies['title_ids'].tolist()
        parent_directory = os.getcwd()
        for title in movies_list:
            crew_dictionary = imdb_scraper.get_full_crew_for_movie(title, set_imdb_details=True)
            full_directory_path_ids = os.path.join(parent_directory, id)
            if os.path.isdir(full_directory_path_ids):
                full_directory_path = os.path.join(full_directory_path_ids, '{}_movies'.format(id))
                if not os.path.exists(full_directory_path):
                    os.makedirs(full_directory_path)
                json_file_path = os.path.join(full_directory_path, '{}.json'.format(title))
                if not os.path.exists(json_file_path):
                    with open(json_file_path, 'w') as json_file:
                        json.dump(crew_dictionary, json_file)

def process_json_file(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        title_uri = data.get("title_uri", "")
        title = data.get("title", "")
        
        # Extract full credits
        full_credits = []
        for credit_entry in data.get("full_credits", []):
            role = credit_entry.get("role", "")
            for crew_member in credit_entry.get("crew", []):
                name = crew_member.get("name", "")
                link = crew_member.get("link", "")
                credit = crew_member.get("credit", "")
                full_credits.append({
                    "Title": title,
                    "Title_URI": title_uri,
                    "Role": role,
                    "Name": name,
                    "Link": link,
                    "Credit": credit
                })
        
        return full_credits

def write_to_csv(data, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Title_URI', 'Role', 'Name', 'Link', 'Credit']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def full_credits():
    parent_directory = os.getcwd()
    all_credits = []
    directories_list = os.listdir(parent_directory)
    for directory in directories_list:
        if 'nm' in directory:
            path_1 = os.path.join(parent_directory, directory)
            path_2 = os.path.join(path_1, '{}_movies'.format(directory))
            if os.path.exists(path_2):
                for files in os.listdir(path_2):
                    if files.endswith('.json'):
                        json_file_path = os.path.join(path_2, files)
                        credits = process_json_file(json_file_path)
                        all_credits.extend(credits)
    return all_credits


def __name__ == "__main__":
    csv_file = sys.argv[0]
    df = pd.read_csv(csv_file)
    director_ids = list(df['director_ids'].unique())
    title_ids_list = df['title_ids'].to_list()
    
    movies_json(director_ids, df)
    feature_film = []

    for title_id in title_ids_list:
        if imdb_scraper.is_feature_film_v2(title_id):
            print(title_id)
            feature_film.append(title_id)

    all_credits = full_credits()
    csv_file_path = 'full_crew_credits.csv'
    write_to_csv(all_credits, csv_file_path)