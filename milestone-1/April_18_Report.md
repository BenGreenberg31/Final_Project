## Network Newts Final Project Report No. 1
Date: April 18, 2024

## Data Collection: Tiffany
> Finished majority of data collection, ran into some problems with certain directors. However, have scraped majority of directors and their credits. Starting to clean up and fix data as well as go back and fix up some code, however have already shared raw data with group members.

Some code used:
```python
# Function that takes in a csv file and tries to find the urls.
def find_urls_in_csv(csv_file):
    urls = []
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for cell in row:
                # Using regular expression to find URLs in each cell
                urls_in_cell = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', cell)
                urls.extend(urls_in_cell)
    return urls

# Function that takes in the list of urls and extracts the ids
def extract_ids(urls):
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

# Function that takes a list of ids and scrapes each id and returns a new folder and a json file (this was used for the directors)
def read_dir_ids(director_ids):
  for id in director_ids:
    credits_dictionary = imdb_scraper.get_full_credits_for_director(id)
    directory = id
    if not os.path.exists(directory):
        os.makedirs(directory)
        json_file_path = os.path.join(directory, '{}.json'.format(id))
        with open(json_file_path, 'w') as json_file:
            json.dump(credits_dictionary, json_file)

# Function that reads json files and returns the data
def read_json_files_from_directory(directory):
    json_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                json_data.append(data)
    return json_data

```
## Network Generation: Becca
Disscussed ideas for network generation. Created plans for some intial networks to create.

## Visualization: Katie
Plan to use gephi to visualize. Will enable filtering by attributes - particularly highlight by crew member, by director, by project to examine director's influence across different crew members and the connections crew members have had.

## Analysis: Ben
Planning to use mostly python and some networkx functionality to conduct analysis. Unsure of exactly what it will look like as of right now. Discussed a lot about rough approach to answer questions like some sort of metric for quantifying director influence - look at number of projects before working with a certain director and then number of projects after working with a certain director (What directors created the most other opportunities for their crew memebers). We also discussed weighting roles by importance (Supervisor roles weighted higher) and scoring strength of relationship (number of times worked together). If we have roles weighted by importance then we can map trajectories of careers to answer the question of how careers of crew members fluctuate. We also thought about Looking at pairs or groups of crew members that worked together maybe employing some sort of community detection algorithm.
