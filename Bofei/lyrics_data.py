import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import time
import re

class Lyrics():
    def getData(self):
        # Read and preprocess data
        df1 = pd.read_csv('../Shaoling/track_lyrics_1.0/track_lyrics_1.csv')
        df2 = pd.read_csv('../Shaoling/track_lyrics_1.0/track_lyrics_2.csv')
        df3 = pd.read_csv('../Shaoling/Billboard_lyrics_2720.csv')
        df = pd.read_csv('Billboard Data/Billboard_with_Spotify_features.csv')
        bb = pd.read_csv('Billboard Data/billboard_2014_to_current.csv')
        # find tracks that are unique on billboard
        tracks = df.title.unique()
        df3.dropna(inplace = True)
        billboard_lyrics = df1.loc[df1.track_name.isin(tracks)]\
        .append(df2.loc[df2.track_name.isin(tracks)])
        # selected features
        features = [
         'title',
         'Spotify_ID',
         'Spotify_Popularity',
         'Is_Explicit',
         'acousticness',
         'danceability',
         'energy',
         'instrumentalness',
         'liveness',
         'loudness',
         'mode',
         'speechiness',
         'tempo',
         'valence']
        # drop duplicates items
        df = df[features].drop_duplicates()
        df.dropna(inplace = True)
        # unused columns
        billboard_lyrics.drop('Unnamed: 0',axis = 1,
                             inplace = True)
        # for combining two models 
        features_filter = ['Spotify_ID', 'Spotify_Popularity', 'Is_Explicit',
               'acousticness', 'danceability', 'energy', 'instrumentalness',
               'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'valence', 'lyrics', 'Label']
        positive_class = pd.merge(df,billboard_lyrics,left_on='title',
                right_on = 'track_name')
        
        positive_class['Label'] = 1
        positive_class = positive_class[features_filter]
        negative_class = pd.read_csv('Billboard Data/tracks_with_audio_features.csv')
        # negative class are from different API calling, so column name is different
        negative_class.rename({'id':'Spotify_ID',
                               'popularity':'Spotify_Popularity',
                               'name':'title',
                              'release_date':'Spotify_release_Date',
                              'explicit':'Is_Explicit'},axis = 1,
                             inplace = True)
        
        negative_class = negative_class[features]
        
        # to make it accurate, drop the duplicate items in this dataset
        # since audio features should not be duplicated with other id
        
        temp = pd.merge(negative_class,df1[['track_name','lyrics']],
                left_on = 'title',
                right_on = 'track_name')
        songs_wrong = (temp.title.value_counts().loc[temp.title.value_counts() >= 2]).index
        print(temp.shape)
        temp = temp.loc[~temp.title.isin(songs_wrong)]
        print(temp.shape)
        
        negative_class = temp
        del temp
        negative_class = negative_class\
        .loc[~negative_class.Spotify_ID.isin(positive_class.Spotify_ID)]
        # remove all missing value and duplicates rows 
        negative_class['Label'] = 0
        negative_class = negative_class[features_filter]
        negative_class.dropna(inplace = True)
        positive_class.dropna(inplace = True)
        negative_class.drop_duplicates(inplace = True)
        positive_class.drop_duplicates(inplace = True)
        # assign label for positive class
        df3['Label'] = 1
        positive_class = df3[positive_class.columns]
        return positive_class , negative_class
    
    
    def getDataFilteredByRe(self,positive_class,negative_class):
        numeric_features = ['Spotify_Popularity', 'Is_Explicit',
        'acousticness', 'danceability', 'energy', 'instrumentalness',
        'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'valence', 'Label']
        audio_features = ['acousticness', 'danceability', 'energy', 'instrumentalness',
        'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'valence']
        model_data = positive_class[['Spotify_ID','lyrics','Label'] + audio_features]\
        .append(negative_class[['Spotify_ID','lyrics','Label'] + audio_features]\
                .sample(n = positive_class.shape[0]))
        print(model_data.Label.value_counts())
        
        # count vector for the lyrics
        countVect = CountVectorizer(binary = True,stop_words='english',
                                   ngram_range = (1,2))
        print('Removing stop words of lyrics')
        model_data['lyrics'] = [str(i) for i in model_data['lyrics']]
        model_data['lyrics'] = model_data['lyrics'].str.replace('\n',' ')
        model_data['lyrics'] = model_data['lyrics'].str.replace(r'\d+','') # remove digits.
        model_data['lyrics'] = model_data['lyrics'].str.replace('_',' ') # remove under score
        model_data['lyrics'] = model_data['lyrics'].str.replace('Yeah','')
        model_data['lyrics'] = model_data['lyrics'].str.replace('yeah','')
        model_data['lyrics'] = model_data['lyrics'].str.replace(r"[\(\[].*?[\)\]]",'')
        # set index if not done
        model_data.set_index('Spotify_ID',inplace = True)
        
        return model_data