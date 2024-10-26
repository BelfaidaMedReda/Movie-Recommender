#!/usr/bin/env python
# coding: utf-8

# ### Movie Recommander System project

# In[1]:


import pandas as pd 
import numpy as np


# In[2]:


movies = pd.read_csv("dataset/movies.csv")
credits = pd.read_csv("dataset/credits.csv")


# In[3]:


movies.head(2)


# In[4]:


credits.head(2)


# In[5]:


# Merging between movies dataset and credits one
movies = movies.merge(credits,left_on="id",right_on="movie_id")


# In[6]:


# Select the key features for the project
movies = movies[["id","genres","keywords","title_x","overview","cast","crew"]].rename(columns={"title_x":"title"})


# In[7]:


# Kicking out records with null value
movies.isnull().any()
movies = movies.dropna()


# In[8]:


movies = movies.drop_duplicates()


# In[9]:


# Converting Json strings in genres and keywords attributes to ordinary list

import json

def convert(json_ch):
    res = []
    tab = json.loads(json_ch)
    for elem in tab:
        res.append(elem["name"])
    return res

movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)


# In[10]:


# Targeting cast attribute

def choose3(json_ch):
    res = []
    L = json.loads(json_ch)
    count = 0 
    for x in L:
        if count < 3 :
            res.append(x["name"])
            count+=1
        else:
            break
    return res

movies["cast"] = movies["cast"].apply(choose3)


# In[11]:


# Targeting crew attribute

def choose_director(json_ch):
    res = []
    L  = json.loads(json_ch)
    for x in L : 
        if x["job"] == "Director":
            res.append(x["name"])
    return res

movies["crew"] = movies["crew"].apply(choose_director)


# In[12]:


#Targeting overview attribute

def aslist(ch):
    return ch.split(" ")

movies["overview"] = movies["overview"].apply(aslist)


# In[13]:


movies.head(5)


# In[14]:


# Eliminating spaces in genres, keywords, cast and crew

def nospace(L):
    return [elem.replace(" ","") for elem in L]

for elem in ("genres" , "keywords" , "cast" , "crew"):
    movies[elem] = movies[elem].apply(nospace)


# In[15]:


# Creating tag attribute & adding new dataframe
movies["tag"] = movies["overview"] + movies["genres"] + movies["keywords"] + movies["cast"] + movies["crew"]
new_df = movies[["id" , "title" , "tag"]]
new_df.head(5)

new_df["tag"] = new_df["tag"].apply(lambda x:" ".join(x))


# In[16]:


new_df["tag"] = new_df["tag"].apply(lambda x: x.lower())


# In[17]:


new_df.head()


# In[18]:


from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer

import nltk

# Download necessary resources if they aren't already downloaded
nltk.download('stopwords')
nltk.download('punkt')

class StemmedCountVectorizer(CountVectorizer):

    def build_analyzer(self):
        analyzer = super().build_analyzer()
        ps = PorterStemmer()  # Corrected the class name here
        return lambda doc: [ps.stem(word) for word in analyzer(doc)]


# In[19]:


new_df.shape


# In[21]:


# We make a choice of 5000 relevant words so it doesn't crash in future computations
SVC = StemmedCountVectorizer(stop_words='english',max_features=5000)

BOW_matrix = SVC.fit_transform(new_df["tag"]).toarray()
vocabulary = SVC.get_feature_names_out()

print("vocabulary length is",len(vocabulary))
print(BOW_matrix)


# In[26]:


import string

def remove_punctuation_and_extra_spaces(text):
    # Remove punctuation
    text_without_punctuation = text.translate(str.maketrans('', '', string.punctuation))
    # Remove extra spaces and return the cleaned text
    return ' '.join(text_without_punctuation.split())

new_df["tag"] = new_df["tag"].apply(remove_punctuation_and_extra_spaces)


# In[28]:


# We will stem the tags

ps =  PorterStemmer()

def stem(text):
    res=[]
    words=text.split(" ")
    for word in words:
        res.append(ps.stem(word))
    return " ".join(res) 

new_df["tag"] = new_df["tag"].apply(stem)


# In[32]:


# We will delete the stopwords from the text
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

stop_words = set(stopwords.words('english'))

def remove_SW(text):
    textList = text.split(" ")
    text_tokens = word_tokenize(text)
    filtered_text = " ".join([word for word in text_tokens if word not in stop_words])
    return filtered_text

new_df["tag"] = new_df["tag"].apply(remove_SW)


# In[39]:


# Let's compute similarities 
from sklearn.metrics.pairwise import cosine_similarity

n = len(BOW_matrix)

def recommend(movie):
    """
    This function provides five recommended movies based on the cosine similarity
    metric using a bag-of-words representation.
    """
    # Get the index of the movie in the DataFrame
    try:
        movie_index = new_df.index[new_df['title'] == movie][0]
    except IndexError:
        return "Movie not found in the dataset."

    # Calculate cosine similarities for all movies with the specified movie
    similarities = [
        (index, cosine_similarity(BOW_matrix[movie_index].reshape(1, -1), BOW_matrix[index].reshape(1, -1))[0][0])
        for index in range(n) if index != movie_index
    ]
    
    # Sort by similarity in descending order
    similarities = sorted(similarities, reverse=True, key=lambda elem: elem[1])

    # Get the top 5 most similar movies
    recommended_indices = [index for index, similarity in similarities[:5]]
    recommended_titles = new_df.iloc[recommended_indices]["title"].tolist()

    return recommended_titles

# Testing the function for 
print(recommend("Avatar"))

