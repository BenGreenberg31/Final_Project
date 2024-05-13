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

# Print descriptive statistics
print(descriptive_stats)

print(sorted_directors.shape[0])