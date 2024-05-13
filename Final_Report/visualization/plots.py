import os
import matplotlib.pyplot as plt
import pandas as pd

directors_movies_df = pd.read_csv('directors_movies.csv')
final_credits_df = pd.read_csv('final_credits.csv')

# Number of featured movies
num_featured_movies = final_credits_df['Title'].unique()

# Number of directors
num_directors = directors_movies_df['director_name'].nunique()

# Number of movies per director
movies_per_director = directors_movies_df.groupby('director_name')['title'].nunique().sort_values(ascending = False)
print(type(movies_per_director))
print(movies_per_director)

top_ten_dirs = movies_per_director.head(10)
print(top_ten_dirs)
# Average number of movies per director
avg_movies_per_director = movies_per_director.mean()

# Number of crews
num_crews = final_credits_df['Name'].nunique()

# Number of roles and frequency of each role
num_roles = final_credits_df['Role'].nunique()

roles_frequency = final_credits_df['Role'].value_counts()


# distribution of movies made by director
plt.figure() 
plt.plot(movies_per_director)
plt.axhline(y= 30.386138613861387, color='r', linestyle='-')
plt.title('Distribution of Number of Movies Per Director')
plt.xticks([])
plt.xlabel('Directors')
plt.ylabel('Number of Movies')
plt.savefig('director_distn_plt.png')

# num movies made by top ten dirs
plt.figure()
top_ten_dirs.plot.bar()
plt.ylabel('Number of Movies')
plt.xlabel('Director')
plt.title('Number of Movies Made by Top Ten Directors')
plt.subplots_adjust(bottom=0.35)
plt.axhline(y= 30.386138613861387, color='r', linestyle='-')
plt.savefig('top_ten_dirs_plot.png')

# num people in each role
plt.figure()
roles_frequency.plot.bar()
plt.title('Frequency of Roles')
plt.ylabel('Number of Crew')
plt.subplots_adjust(bottom=0.4)

plt.savefig('freq_of_roles_plot.png')
# plt.plot(size_list, insert_list, label = 'Insertion Sort', marker = 'o', color = 'blue')
# plt.plot(size_list, select_list, label = 'Selection Sort', marker = 'o', color = 'red')
# plt.xlabel('Array Size')
# plt.ylabel('Count')
# plt.legend(loc="lower right")
