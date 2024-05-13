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

## Visualization: Katie

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

Research Questions

Measure how roles of crew members fluctuate?

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

How widespread is the phenomenon of directors re-using the same crew? Do renowned directors (and women/minority directors) tend to work persistently with the same key collaborators compared to lesser recognized directors or a [random Hollywood director](100_rand_hollywood_dir.txt)? 

## Research Questions/Tasks

* Analyses was provided to understand the composition of dataset
* Analyses was provided to address relevant research questions
* Analysis is sound and code provided for computing metrics. Documented (comments and Readmes) Python scripts (not Notebooks) were used. Code is modular (uses separate files/functions) and reusable (no hard-coding). 
* Report includes problem summary/questions, code snippets, and is clearly written: well-organized and includes few typos/grammatical errors

### References
* https://www.geeksforgeeks.org/python-itertools-combinations-function/
* https://www.geeksforgeeks.org/how-to-calculate-jaccard-similarity-in-python/
