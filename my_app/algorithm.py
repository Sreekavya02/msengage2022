import ast
import numpy as np
import pandas as pd
import os.path
from pathlib import Path
import requests
pd.options.mode.chained_assignment = None  # default='warn'

BASE_DIR = Path(__file__).resolve().parent

file1path=os.path.join(BASE_DIR,'csvfiles_fordf/tmdb_5000_movies.csv')
file2path=os.path.join(BASE_DIR,'csvfiles_fordf/tmdb_5000_credits.csv')

credits=pd.read_csv(file2path);
movies=pd.read_csv(file1path);

movies=movies.merge(credits,on='title')

movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)

def convert(unfilteredlist):
    L=[]
    for item in ast.literal_eval(unfilteredlist):
        L.append(item['name'])
    return L

def convertcast(unfilteredlist):
    L=[]
    count=0
    for item in ast.literal_eval(unfilteredlist):
        if count<3:
            L.append(item['name'])
            count+=1
        else:
            break
    return L

def getdirector(unfilteredlist):
    L=[]
    for item in ast.literal_eval(unfilteredlist):
        if item['job'] == 'Director':
            L.append(item['name'])
            break
    return L

movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)
movies['cast']=movies['cast'].apply(convertcast)
movies['crew']=movies['crew'].apply(getdirector)

movies['overview']=movies['overview'].apply(lambda x:x.split())

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])


def get_genreMovies():
    actionMovies = []
    adventureMovies=[]
    thrillerMovies=[]
    romanceMovies=[]
    crimeMovies=[]
    scfictionMovies=[]
    fantasyMovies=[]
    dramaMovies=[]
    animationMovies=[]
    n = len(movies.index)
    for ind in range(n):
        genres = movies.iloc[ind]['genres']
        if len(genres) != 0:
            if genres[0] == 'Action':
                actionMovies.append(movies.iloc[ind]['movie_id'])
            elif genres[0] == 'Adventure':
                adventureMovies.append(movies.iloc[ind]['movie_id'])
            elif genres[0] == 'Thriller':
                thrillerMovies.append(movies.iloc[ind]['movie_id'])
            elif genres[0] == 'Romance':
                romanceMovies.append(movies.iloc[ind]['movie_id'])
            elif genres[0] == 'Crime':
                crimeMovies.append(movies.iloc[ind]['movie_id'])
            elif genres[0] == 'ScienceFiction':
                scfictionMovies.append(movies.iloc[ind]['movie_id'])
            elif genres[0] == 'Fantasy':
                fantasyMovies.append(movies.iloc[ind]['movie_id'])
            elif genres[0] == 'Drama':
                dramaMovies.append(movies.iloc[ind]['movie_id'])
            elif genres[0] == 'Animation':
                animationMovies.append(movies.iloc[ind]['movie_id'])

    return actionMovies,adventureMovies,thrillerMovies,romanceMovies,crimeMovies,scfictionMovies,fantasyMovies,dramaMovies,animationMovies


#Fantasy Crime Thriller Drama Animation Family Romance ScienceFiction Action Adventure



movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']

finalmovies=movies[['movie_id','title','tags']]

finalmovies['tags']=finalmovies['tags'].apply(lambda x:" ".join(list(x)))
finalmovies['tags']=finalmovies['tags'].apply(lambda x:x.lower())

import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stemming(text):
    stemmedtext=[]
    for i in text.split():
        stemmedtext.append(ps.stem(i))
    return " ".join(stemmedtext)

finalmovies['tags']=finalmovies['tags'].apply(stemming)

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')

vectors=cv.fit_transform(finalmovies['tags']).toarray()

from sklearn.metrics.pairwise import cosine_similarity

similarity_model=cosine_similarity(vectors)

def recommend(movie):
    movie_index=finalmovies[finalmovies['title']==movie].index[0]
    movie_id=finalmovies.iloc[movie_index].movie_id;
    recommendedmoviesindexes=sorted(list(enumerate(similarity_model[movie_index])),reverse=True,key=lambda x:x[1])[1:11]
    recommendedmoviesids=[]
    for i in recommendedmoviesindexes:
        recommendedmoviesids.append(finalmovies.iloc[i[0]].movie_id)
    return movie_id,recommendedmoviesids

def gettitles():
    return finalmovies['title']

def fetch_details(movieid):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9efcaddf4cc2015dfec426a229f2768d'.format(movieid))
    data=response.json()
    data['poster_path']= "https://image.tmdb.org/t/p/w500/"+data['poster_path']
    return data

###################################################