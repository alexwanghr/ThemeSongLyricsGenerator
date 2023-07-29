import json
import requests
import urllib
import csv
import pandas as pd
from pathlib import Path

# API Key
api_key = "6fdd7aa0"
# OMDb API
OMDb_url = "http://www.omdbapi.com/?i=tt3896198&apikey=6fdd7aa0"
# TMDB API
TMDB_url = "https://api.themoviedb.org/3/search/movie?query="
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3NmFlZDBjYjc2YThhNWVkZDY3OTE1NTJjODc0YWVlOCIsInN1YiI6IjY0NmZiNmI3YzVhZGE1MDEzNTgzNzQ2ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.umBLtRSOFidJwK_LqVonu4T7KhenkC9MYWdKlLyN0rI"
}
# collect plot data storing path
plot_path = Path("plot")
# make sure the folder exists
plot_path.mkdir(parents=True, exist_ok=True)

csv_file = "movies.csv"
theme_titles = ["Spiderman","Star Wars", "Pirates of the Caribbean"]


# file = csv.DictReader(open(csv_file, 'r'))
 
# iterating over each row and append
# for col in file:
#     if col['Spiderman']:
#         spiderman_titles.append(col['Spiderman'])
#     movies_dict['Spiderman'] = spiderman_titles


movies_titles_dict = {}
df = pd.read_csv(csv_file, encoding= 'unicode_escape',index_col=False)
for theme in theme_titles:
    movies_titles_dict[theme] = df[theme].tolist()
    

# Get json data by titles and processed data formats
def get_plot_data(theme):
    collect_data = []
    for title in movies_titles_dict[theme]:
        title = str(title)
        if title!='nan':
            year = title[0:4]
            name = title[4:]
            request_url = OMDb_url+'&t='+name+'&y='+str(year)+"&plot=full"
            movieInfo = requests.get(request_url).json()
            
             # Get rid of data which not found
            if movieInfo["Response"] == 'True':
                lines = movieInfo["Plot"].split('.')
                for line in lines:
                    collect_data.append(line)
    
    print("OMDB")
    print(collect_data)
    return collect_data
            

def get_from_TMDB(title):
    txt='N/A'
    year = title[0:4]
    name = title[4:]
    name = name.replace(" ","-")
    url = TMDB_url+ name + "&include_adult=false&language=en-US&page=1&year="+year+"&plot=full"
    response = requests.get(url, headers=headers).json()
    for result in response["results"]:
        if result["original_title"]==name:
            txt=result["overview"]
            break
        else:
            if result['release_date'][0:4]==year:
                txt=result["overview"]
                break
    return txt


def get_plot_data_tmdb(theme):
    collect_data_tmdb=[]
    for title in movies_titles_dict[theme]:
        title = str(title)
        if title != "nan":
            year = title[0:4]
            name = title[4:]
            movieInfo = get_from_TMDB(title)
            lines = movieInfo.split('.')
            for line in lines:
                collect_data_tmdb.append(line)
    print("TMDB")
    print(collect_data_tmdb)
    return collect_data_tmdb


for theme in theme_titles:
    plot_omdb = get_plot_data(theme)
    plot_tmdb = get_plot_data_tmdb(theme)
    plot = plot_omdb + plot_tmdb
    file_name = theme+'_plot.json'
    file_path = plot_path / file_name
    with open(file_path, 'w') as outfile:
        json_string = json.dumps(plot)
        outfile.write(json_string)
