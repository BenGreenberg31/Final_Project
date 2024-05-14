import os
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations
import numpy as np
import pandas as pd
from collections import Counter

# Basic Analysis Questions
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

# Jaccard Similarity Calculations
from itertools import combinations
import numpy as np
import pandas as pd
#from sklearn.metrics import jaccard_score

final_credits = pd.read_csv('final_credits.csv')
directors_movies = pd.read_csv('directors_movies.csv')


# Map all title_ids to crew
crew_dict = final_credits.groupby('title_id')['Name'].apply(set).to_dict()

# Jaccard similarity score function from GeeksForGeeks
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0


directors = directors_movies.groupby('director_name')
director_similarity_scores = {}

# Decided to calculate the jaccard similarity for every combination of crews and then average those similarity scores for each director

for director, group in directors:
    title_ids = group['title_ids'].dropna().unique()
    if len(title_ids) > 1:
        scores = []
        
        for title_id1, title_id2 in combinations(title_ids, 2):
            crew1 = crew_dict.get(title_id1, set())
            crew2 = crew_dict.get(title_id2, set())
            score = jaccard_similarity(crew1, crew2)
            scores.append(score)

        director_similarity_scores[director] = np.mean(scores)
    
    else:
        # If a director only has one project set the similarity to 0
        director_similarity_scores[director] = 0



sorted_directors = pd.DataFrame(list(director_similarity_scores.items()), columns=['Director', 'Average Jaccard Similarity']).sort_values(by='Average Jaccard Similarity', ascending=False)

#show top directors
print(sorted_directors.head(10))

descriptive_stats = sorted_directors['Average Jaccard Similarity'].describe()

# plotting directors' jaccard similarity
plt.figure()
plt.plot(sorted_directors['Director'], sorted_directors['Average Jaccard Similarity'])
plt.title('Jaccard Similarity of Directors')
plt.ylabel('Jaccard Similarity Score')
plt.xticks([])
plt.savefig('jaccard_plot.png')

# plotting top ten directors' jaccard similarity
plt.figure()
plt.bar(sorted_directors.head(10)['Director'], sorted_directors.head(10)['Average Jaccard Similarity'])
plt.title('Jaccard Similarity of Directors')
plt.ylabel('Jaccard Similarity Score')
plt.xlabel('Director')
# plt.xticks([])
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.3)
plt.savefig('jaccard_bar_plot.png')


# Plotting average role change

dict = {'Makeup Department': 99.75,'Visual Effects by': 99.03,'Sound Department': 98.45,'Casting By': 97.97,
'Special Effects by': 97.78, 'Costume Design by': 97.11, 'Production Design by': 96.17, 'Music by': 94.35,
'Cinematography by': 91.39, 'Produced by': 84.80, 'Writing Credits': 79.20, 'Directed by': 47.06}

plt.figure()
plt.barh(range(len(dict)), list(dict.values()), align='center')
plt.yticks(range(len(dict)), list(dict.keys()),rotation=45, ha='right')
plt.title('Likelihood of crew members exclusively doing each role')
plt.ylabel('Role')
plt.xlabel('Likelihood (%)')
plt.subplots_adjust(left=0.2, bottom = 0.2)

plt.savefig('average_role_change.png')
