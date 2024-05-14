import pandas as pd

# What is the distribution of entities in the director-crew dataset:
# Number of featured movies?
# Number of directors, number movies per director, and average number of movies per director?
# Number of crews members?
# Number of roles and frequency of each role?

import pandas as pd

directors_movies_df = pd.read_csv('directors_movies.csv')
final_credits_df = pd.read_csv('final_credits.csv')

# Number of featured movies
num_featured_movies = final_credits_df['Title'].nunique()

# Number of directors
num_directors = directors_movies_df['director_name'].nunique()

# Number of movies per director
movies_per_director = directors_movies_df.groupby('director_name')['title'].nunique()

# Average number of movies per director
avg_movies_per_director = movies_per_director.mean()

# Number of crews
num_crews = final_credits_df['Name'].nunique()

# Number of roles and frequency of each role
num_roles = final_credits_df['Role'].nunique()

roles_frequency = final_credits_df['Role'].value_counts()


print("Number of featured movies:", num_featured_movies)
print("Number of directors:", num_directors)
print("Number of movies per director:")
print(movies_per_director)
print("Average number of movies per director:", avg_movies_per_director)
print("Number of crews:", num_crews)
print("Number of roles and frequency of each role:")
print("Number of roles: ",num_roles)
print(roles_frequency)
