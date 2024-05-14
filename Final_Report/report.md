# Network Newts Final Project Report: Milestone 3
Date: May 14, 2024

##### Grading rubric

* Report includes project topic summary and research questions. 
* Report addresses research questions.
* Report is well-organized and includes few typos/grammatical errors
* Report includes code snippets, and Github repo includes all code, data, and resources used in project.
* Repo Python scripts (not Notebooks) are well-documented (have comments and ReadMes). Code is modular (uses separate files/functions) and reusable (no hard-coding). 
* Presentation slides are well-organized and include images and code snippets to assist illustration and explanations.
* Presenters effectively communicated their solution to class

Answer all:
1. What is the distribution of entities in the director-crew dataset:
  * Number of featured movies? 
  * Number of directors, number movies per director, and average number of movies per director?
  * Number of crews?
  * Number of roles and frequency of each role?
2. How will you characterize the film-director network? What are the properties (degree dist., average shortest path length, triangles aka clustering coefficient, density/sparcity)?

Pick two questions:
1. Investigate and quantify how directors have influenced the careers of crew members. Clue: consider mapping the careers of crew members over time and see if they experienced significant success after working with a particular director. What directors have had the most influence on crew members?
2. Measure how roles of crew members fluctuate
3. How widespread is the phenomenon of directors re-using the same crew? Do renowned directors (and women/minority directors) tend to work persistently with the same key collaborators compared to lesser recognized directors or a [random Hollywood director](100_rand_hollywood_dir.txt)? 


## Data Collection: Tiffany

## Network Generation: Becca
I decided to create two networks. Both networks are directed with links from crew members to directors. The first network has one link per crew member/director pair and each link is weighted by the number of projects the pair has worked on together. The second network has a one link per project for each crew member/director pair. This links carry the attribute data for the year or the project and the role the crew member held.

The first step in network generation was preparing the data. I merged the directors_movies and final_credits datasets into one data frame and removed duplicate information.

```python
# load data
df1 = pd.read_csv('/content/directors_movies.csv',header=0)
df2 = pd.read_csv('/content/final_credits.csv', header=0)

#match column names
df1=df1.rename(columns={"title_ids": "title_id"})

# create one df
merged_df = pd.merge(df2, df1, on='title_id',how='left')

# drop duplicate columns
merged_df=merged_df.drop(columns=["title"])

# drop directors
merged_df= merged_df.drop(merged_df[merged_df['Role']=="Directed by"].index)
```
Next I created the weigted network:
```python
#Creating weighted network
G = nx.DiGraph()
#add nodes
G.add_nodes_from(merged_df['Name'])
G.add_nodes_from(merged_df['director_name'])

for index, row in merged_df.iterrows():
  if G.has_edge(row[3], row[10]):
      # edge already exists, increase weight by one
      G[row[3]][row[10]]['weight'] += 1
  else:
      # add new edge with weight 1
      G.add_edge(row[3], row[10], weight = 1)
#save network
nx.write_gexf(G, "/content/director_crew_weighted.gexf")
```
Then I created the attribute network
```python
#creating attribute network
G2 = nx.MultiDiGraph()
#add nodes
G2.add_nodes_from(merged_df['Name'])
G2.add_nodes_from(merged_df['director_name'])
edge_number=0
#create edges with attributes
for index, row in merged_df.iterrows():
  G2.add_edge(row[3], row[10], key=edge_number)
  attrs = {(row[3], row[10], edge_number): {"Year": row[8], "Role": row[2]}}
  nx.set_edge_attributes(G2, attrs)
  edge_number += 1
#save network
nx.write_gexf(G2, "/content/attributes.gexf")
```
## Visualization: Katie
Visualizing such a larger network is difficult. I decided to break graphing the network down to question-specific visualizations, rather than simply showing the huge mass of nodes and edges that is the full network. For network visualizations, I decided to use Gephi for ease of user experience, rather than trying to pull apart and format the network using networkx. In addition, I provide many visualizations to support the analysis conducted by Ben. To look at the full network, we have something like the visualization shown below. It's messy, to spread it out even more would make the visualization huge. It is cool to see, however, and we see that there are pockets of crew that are only connected to one director in the outer edges of the network. These nodes include Denis Villenueve (a Canadian filmmaker), cinematographer Sergio Armstrong, queer filmmaker Gregg Araki, and many others.
![full_network](https://github.com/BenGreenberg31/Final_Project/assets/129798383/b36aa699-dd24-456a-ba5d-cd2fa9db1e76)

To focus in on these directors and compare them to others, I used the ego network in Gephi to visualize their networks of crew. For example, we have Woody Allen, the director with the highest Jaccard similarity:
![woody_allen_ego](https://github.com/BenGreenberg31/Final_Project/assets/129798383/14539e66-a4a2-4f88-9a16-f7adb4798e03)
We can compare this ego network, of a very prominent director, to that of Gregg Araki, a much smaller director, who is an outlier in the network and has a pocket of crew connected to the rest of the network through him. 
![gregg_araki_ego](https://github.com/BenGreenberg31/Final_Project/assets/129798383/318d4c6b-de99-4311-962e-3d1165b83549)

Otherwise, I focused on writing a script to create visualizations based on the analysis work. I plotted overall distributions using line charts and focused in on top ten directors in a few cases by highlighting that segment of the distribution with a bar chart. For example, the following code chunk visualizes the jaccard similarity distribution of all the directors in the network.

```python
plt.figure()
plt.plot(sorted_directors['Director'], sorted_directors['Average Jaccard Similarity'])
plt.title('Jaccard Similarity of Directors')
plt.ylabel('Jaccard Similarity Score')
plt.xticks([])
plt.savefig('jaccard_plot.png')
```
To see a smaller view of these numbers, the following code chunk uses matplotlib to generate a bar chart of the Jaccard similarity of the ten directors with the highest Jaccard similarity score.

```python
plt.figure()
plt.bar(sorted_directors.head(10)['Director'], sorted_directors.head(10)['Average Jaccard Similarity'])
plt.title('Jaccard Similarity of Directors')
plt.ylabel('Jaccard Similarity Score')
plt.xlabel('Director')
# plt.xticks([])
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.3)
plt.savefig('jaccard_bar_plot.png')
```
## Analysis: Ben
## Analysis: Ben
To answer the first questions relating to what is the distribution of entities in the director-crew dataset I wrote a simple script which can be found in the statistic_check.py file within the final_report folder. The results that it yielded are shown below

1.What is the distribution of entities in the director-crew dataset:

Number of featured movies?
* 1264

Number of directors, number movies per director, and average number of movies per director?
* There are 101 directors in the dataset, and the average number of movies per director is 30.39
* The number of movies that each director has made can be found by running the python file

Number of crews?
* There are 8137 crew in the dataset

Number of roles and frequency of each role?
* There are 12 roles

| Role | Frequency |
| ------ | ------- |
|Writing Credits |        3567|
|Produced by     |        3222|
|Sound Department   |     2865|
|Visual Effects by  |     2636|
|Directed by       |      2214|
|Casting By       |       1863|
|Cinematography by   |    1750|
|Music by         |       1445|
|Production Design by  |  1298|
|Costume Design by    |   1226|
|Makeup Department   |     701|
|Special Effects by  |     533|

Examining the network properties we found that:

* Average Shortest Path Length: 0.0010628211965840937
* Average Clustering Coefficient:0.037667712870140826
* Density: 0.00022323828449190384
* Sparsity: 0.9997767617155081

```python
#Average shortest path length
avg_shortest_path_length = nx.average_shortest_path_length(G)


G_undirected = G.to_undirected()
#avg clustering coefficient
average_clustering = nx.average_clustering(G_undirected)

density = nx.density(G)

sparsity = 1 - density
```

### Research Questions

#### Measure how roles of crew members fluctuate?

```python
# What percentage of crew members only have one role and for those crew members what are their roles most often?

# counter for crew that only do one role throughout their career
one_role_counter = 0

single_roles = []

tot_crew = df['Name'].nunique()
grouped_by_name = df.groupby('Name')

for name, group_df in grouped_by_name:
    # for each group
    # get the number of unique roles 
    num_roles = group_df['Role'].nunique()
    #print(num_roles)
    #print(group_df)
    # unique_roles == 1
    # update counter variable 
    # store what that role is in a list
    if num_roles == 1:
        one_role_counter += 1
        single_roles.append(group_df['Role'].iloc[0])

percentage = (one_role_counter/tot_crew * 100)
```
Sought to understand what percentage of crew members only have one role for their entire career to better understand the dataset. Also the research question is related to fluctuations of crew member careers so understanding this would tell us how many crew have careers that are static or do not fluctuate between roles.
* Found that the percentage of the 8137 crew members that have only worked in one role throughout their career was 94.99%
* This told us a lot about the dataset and gave us more understanding about the nature of crew careers.
* One of the biggest takeaways is that most crew members are specialized and will not change roles throughout their career. This makes logical sense, as once you build a technical set of skills, say for sound you will most likely continue to work in the department instead of switching to music or cinematography.
* Among those 95% of crew members that have only worked one role the breakdown of roles were as follows

|Role|Percentage of Crew Members|Count of Crew Members|
|----|------|-----|
|Writing Credits| 16.76% |1295|
|Produced by| 15.95% |1233|
|Visual Effects by|14.57% |1126|
|Sound Department|9.85% |761|
|Cinematography by| 7.14% |552|
|Music by|6.26% |484|
|Casting By| 6.25% |483|
|Production Design by| 6.17% |477|
|Costume Design by |5.65% |437|
|Makeup Department| 5.08%| 393|
|Special Effects by| 3.42% |264|
|Directed by|2.90% |224|

* This led us to be curious about the roughly 5 percent of crew members that have switched roles. What roles are the most static and what roles see the most people switch in to them.
* I decided to look at the likelihood that a crew member only worked in a certain role.
* The results are as follows

Likelihood of crew members exclusively doing each role:
* Makeup Department: 99.75%
* Visual Effects by: 99.03%
* Sound Department: 98.45%
* Casting By: 97.97%
* Special Effects by: 97.78%
* Costume Design by: 97.11%
* Production Design by: 96.17%
* Music by: 94.35%
* Cinematography by: 91.39%
* Produced by: 84.80%
* Writing Credits: 79.20%
* Directed by: 47.06%

Most roles have a pretty high likelihood that crew members have only done those roles, especially for the more technical roles, whereas production, writing, and directing were among the lowest, most notably directing was below 50% whereast the next lowest was writing at clost to 80%.

```python
crew_roles = df.groupby(['Name', 'Role']).size().unstack(fill_value=0)

#print(crew_roles)

# Filter crew members who have worked in any role
crew_with_roles = crew_roles[crew_roles.sum(axis=1) > 0]

#print(crew_with_roles.head())

# Calculate the likelihood of each role
role_likelihood = {}
for role in crew_with_roles.columns:
    num_crew_with_role = (crew_with_roles[role] > 0).sum()
    num_crew_only_role = ((crew_with_roles[role] > 0) & (crew_with_roles.sum(axis=1) == crew_with_roles[role])).sum()
    if num_crew_with_role > 0:
        role_likelihood[role] = num_crew_only_role / num_crew_with_role


sorted_roles_likelihood = sorted(role_likelihood.items(), key=lambda x: x[1], reverse=True)
```

* The sort of natural next step is trying to determine how people are moving within these roles. Where are most first time directors coming from, what was their background before that. And for people that are no longer in a role, what are they most likely to do next.

```python
role_transition_to = {role: {} for role in roles_frequency}
role_transition_from = {role: {} for role in roles_frequency}
total_transitions_to = {role: 0 for role in roles_frequency}
total_transitions_from = {role: 0 for role in roles_frequency}

multi_roles_crew = 0

for name, group_df in grouped_by_name:
    # If a crew member had more than one role throughout their career
    # Iterate through the dataframe to record transitions for those crew members
    num_roles = group_df['Role'].nunique()

    if num_roles > 1:
        for i in range(len(group_df) - 1):
            current_row = group_df.iloc[i]
            next_row = group_df.iloc[i + 1]
            current_role = current_row['Role']
            next_role = next_row['Role']
            #print(current_role)
            #print(next_role)
            if current_role != next_role:
                total_transitions_to[current_role] += 1
                total_transitions_from[next_role] += 1
                if next_role in role_transition_to[current_role]:
                    role_transition_to[current_role][next_role] += 1
                else:
                    role_transition_to[current_role][next_role] = 1

                if current_role in role_transition_from[next_role]:
                    role_transition_from[next_role][current_role] += 1
                else:
                    role_transition_from[next_role][current_role] = 1


# aim is to give clearer picture of movement between roles

# calculate the probabilities for transitions to other roles and percentages
role_transition_to_probabilities = {}
for current_role, transitions in role_transition_to.items():
    total_transitions = total_transitions_to[current_role]
    role_transition_to_probabilities[current_role] = {next_role: (count, count / total_transitions * 100) for next_role, count in transitions.items()}

# calculate the probabilities for transitions from other roles and pecetanges
role_transition_from_probabilities = {}
for next_role, transitions in role_transition_from.items():
    total_transitions = total_transitions_from[next_role]
    role_transition_from_probabilities[next_role] = {current_role: (count, count / total_transitions * 100) for current_role, count in transitions.items()}
```

* The biggest takeaway from this analysis was how the flow between Directing, production, and writing dominates, highlighting a trio of roles that often cycle among each other. This definitely highlights the central importance of these roles in career development within the film industry. Other role changes were less notable and those other roles saw higher rates of specialization as show in the earlier analysis
* There is not as much flow between the technical roles but there are some interesting patterns like between production design and costume design.

#### How widespread is the phenomenon of directors re-using the same crew? Do renowned directors (and women/minority directors) tend to work persistently with the same key collaborators compared to lesser recognized directors or a [random Hollywood director](100_rand_hollywood_dir.txt)? 

* For this question I was thinking about various similarity metrics to use and I decided to use the Jaccard Similarity Metric that we had talked about in class. I did some google searching and I found an implementation for a Jaccard Similarity function in python on geeksforgeeks.org

```python
def jaccard_similarity(set1, set2):
    # intersection of two sets
    intersection = len(set1.intersection(set2))
    # Unions of two sets
    union = len(set1.union(set2))
     
    return intersection / union
```
 
* Jaccard similarity is typically used to compute similarity between two sets or groups, but for this use case we have directors with sometimes many more crews than that so I needed a metric that captured similarity between all the crews that a director has used in their career on different projects.
* I decided to calculate the Jaccard similarity for each pair of crews and then average these scores (which I did using the itertools combinations function). This method gives an overall idea of similarity across multiple projects and gives us a way to compare different directors and how similar their crews are from project to project.

```python
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
```

* The full code can be found in the final report folder

#### Results

Directors with the Highest Scores
* Woody Allen: Highest average Jaccard similarity of 0.176311. This suggests that Woody Allen has a strong tendency to reuse the same crew members across his projects more than any other director in this dataset. Joel Coen Follows with a similarity score of 0.148928, indicating significant reuse of crew members. Clint Eastwood, Christopher Nolan, and Kelly Reichardt also show notable similarities in their crews, with scores ranging from 0.094836 to 0.069960, supporting their preference for working with familiar teams.

* These are all notable directors which seems to suggest that the more notable the director the more prevalent the henomena of directors re-using the same crew is. And that makes logical sense that bigger more influential directors would have more sway or choice in who is on their crew. Additionally there might be something to be said for success influencing crew reuse. If a director makes a really succesful movie, they probably would want to employ some of the same crew that helped contribute to that success.

* The mean Jaccard similarity score across all directors is 0.026026 and  suggesting that on average, directors do not often reuse crew members extensively.
* The standard deviation is 0.027091, indicating a moderate variability in crew reuse among directors.
* Directors like Woody Allen and Joel Coen are significant outliers, showing much higher tendencies to reuse crew compared to their peers.
* Most directors have low to moderate similarity scores, indicating that extensive crew reuse is not the norm. The distribution is skewed right, with a few directors showing very high reuse rates.
  
## Research Questions/Tasks

* Analyses was provided to understand the composition of dataset
* Analyses was provided to address relevant research questions
* Analysis is sound and code provided for computing metrics. Documented (comments and Readmes) Python scripts (not Notebooks) were used. Code is modular (uses separate files/functions) and reusable (no hard-coding). 
* Report includes problem summary/questions, code snippets, and is clearly written: well-organized and includes few typos/grammatical errors

### References
* https://www.geeksforgeeks.org/python-itertools-combinations-function/
* https://www.geeksforgeeks.org/how-to-calculate-jaccard-similarity-in-python/
