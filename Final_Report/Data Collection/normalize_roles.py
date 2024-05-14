import imdb_scraper
import sys
import os
import json
import re
import pandas as pd
import csv

def check_feature(title_ids):
    feature_film = []

    for title_id in title_ids:
        if imdb_scraper.is_feature_film_v2(title_id):
            print(title_id)
            feature_film.append(title_id)
    return feature_film

def desired_role(df):
    desired_roles = [
    'Casting By',
    'Cinematography by',
    'Costume Design by',
    'Directed by',
    'Film Editing by',
    'Makeup Department',
    'Music by',
    'Produced by',
    'Production Design by',
    'Sound Department',
    'Special Effects by',
    'Visual Effects by',
    'Writing Credits']

    df_subset = df.loc[df['Role'].isin(desired_roles)]
    return df_subset

def subsetting_department(crew_df_subset):
    crew_df_makeup_department = crew_df_subset[crew_df_subset['Role'] == 'Makeup Department']
    crew_df_makeup_department = crew_df_makeup_department[(crew_df_makeup_department['Credit'] == 'hair department head') | (crew_df_makeup_department['Credit'] == 'makeup department head')]
    crew_df_produced = crew_df_subset[crew_df_subset['Role'] == 'Produced by']
    crew_df_produced = crew_df_produced[(crew_df_produced['Credit'] == 'producer') | (crew_df_produced['Credit'] == 'producer produced by') | (crew_df_produced['Credit'] == 'producer produced by p.g.a.')]
    crew_df_sound = crew_df_subset[crew_df_subset['Role'] == 'Sound Department']
    crew_df_sound = crew_df_sound[(crew_df_sound['Credit'] == 're-recording mixer') | (crew_df_sound['Credit'] == 'sound designer') | (crew_df_sound['Credit'] == 'supervising sound editor')]
    crew_df_se = crew_df_subset[crew_df_subset['Role'] == 'Special Effects by']
    crew_df_se = crew_df_se[(crew_df_se['Credit'] == 'special effects supervisor')]
    crew_df_ve = crew_df_subset[crew_df_subset['Role'] == 'Visual Effects by']
    crew_df_ve = crew_df_ve[(crew_df_ve['Credit'] == 'visual effects supervisor')]
    undesired_values = ['Makeup Department', 'Produced by', 'Sound Department', 'Special Effects by', 'Visual Effects by']
    crew_df_subset = crew_df_subset[~crew_df_subset['Role'].isin(undesired_values)]
    dfs = [crew_df_subset, crew_df_makeup_department, crew_df_sound, crew_df_produced, crew_df_se, crew_df_ve]
    final_df = pd.concat(dfs)
    sorted_df = final_df.sort_values(by='Title')

    return sorted_df
if __name__ == "__main__":
    csv_file = sys.argv[0]
    crew_df = pd.read_csv(csv_file)

    feature_films = check_feature(list(crew_df['title_id']))
    crew_df_subset = crew_df[crew_df['title_id'].isin(feature_film)]
    crew_df_subset['Credit'] = crew_df_subset['Credit'].astype(str)
    crew_df_subset['Credit'] = crew_df_subset['Credit'].astype(str)
    crew_df_subset['Role'] = crew_df_subset['Role'].apply(imdb_scraper.normalize_movie_role)
    crew_df_subset['Credit'] = crew_df_subset['Credit'].apply(imdb_scraper.normalize_crew_credit)

    crew_df_subset = desired_role(crew_df_subset)
    final_df = subsetting_department(crew_df_subset)

    csv_file_path = 'final_credits.csv'
    final_df.to_csv(csv_file_path, index=False)    