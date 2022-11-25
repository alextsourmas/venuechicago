import pandas as pd
import numpy as np 
import streamlit as st
from PIL import Image

#Read in venue data
nightlife_df= pd.read_csv('data/nightlife.csv', index_col='Unnamed: 0') #To csv 
restaurants_df= pd.read_csv('data/restaurants.csv', index_col='Unnamed: 0')
coffee_df= pd.read_csv('data/coffee.csv', index_col='Unnamed: 0')

#Read in nightlife reviews 
nightlife_reviews = pd.read_csv('data/nightlife_reviews.csv', index_col='Unnamed: 0')
nightlife_reviews = nightlife_reviews.reset_index(drop=True)

#Read in restaurant reviews 
# restaurant_reviews_1 = pd.read_csv('data/restaurant_reviews_1.csv', index_col='Unnamed: 0')
# restaurant_reviews_2 = pd.read_csv('data/restaurant_reviews_2.csv', index_col='Unnamed: 0')
# restaurant_reviews_3 = pd.read_csv('data/restaurant_reviews_3.csv', index_col='Unnamed: 0')
# restaurant_reviews_4 = pd.read_csv('data/restaurant_reviews_4.csv', index_col='Unnamed: 0')
# restaurant_reviews = pd.concat([restaurant_reviews_1, restaurant_reviews_2, restaurant_reviews_3, restaurant_reviews_4])
# restaurant_reviews = restaurant_reviews.reset_index(drop=True)

#Read in coffee reviews 
# coffee_reviews = pd.read_csv('data/coffee_reviews.csv', index_col='Unnamed: 0')
# coffee_reviews = coffee_reviews.reset_index(drop=True)

#Read in cosine similarity dfs
nightlife_cosine_sim_df = pd.read_csv('data/nightlife_cosine_sim.csv', index_col='id')
restaurant_cosine_sim_df = pd.read_csv('data/restaurant_cosine_sim.csv', index_col='id')
coffee_cosine_sim_df = pd.read_csv('data/coffee_cosine_sim.csv', index_col='id')

#Preprocess dataframe
nightlife_df['name'] = nightlife_df['name'].astype(str)
nightlife_df['location.address1'] = nightlife_df['location.address1'].astype(str)
nightlife_df['name_and_location'] = nightlife_df[['name', 'location.address1']].agg(': '.join, axis=1)
restaurants_df['name'] = restaurants_df['name'].astype(str)
restaurants_df['location.address1'] = restaurants_df['location.address1'].astype(str)
restaurants_df['name_and_location'] = restaurants_df[['name', 'location.address1']].agg(': '.join, axis=1)
coffee_df['name'] = coffee_df['name'].astype(str)
coffee_df['location.address1'] = coffee_df['location.address1'].astype(str)
coffee_df['name_and_location'] = coffee_df[['name', 'location.address1']].agg(': '.join, axis=1)



st.set_page_config(layout="wide")

with open('style.css') as f: 
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: white;'>Venue Chicago</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>Explore Chicago. Find your new favorite spot.</h3>", unsafe_allow_html=True)
venue_type = st.radio(
    "Which type of venues would you like to find?",
    ('Nightlife', 'Restaurants', 'Coffee Shops'))


def genre_recommendations(i, M, items, k=10):
    """
    Recommends movies based on a similarity dataframe
    Parameters
    ----------
    i : str
        Movie title (index of the similarity dataframe)
    M : pd.DataFrame
        Similarity dataframe, symmetric, with movies as indices and columns
    items : pd.DataFrame
        Contains both the title and some other features used to define similarity
    k : int
        Amount of recommendations to return
    """
    ix = M.loc[:,i].to_numpy().argpartition(range(-1,-k,-1))
    closest = M.columns[ix[-1:-(k+2):-1]]
    closest = closest.drop(i, errors='ignore')
    return pd.DataFrame(closest).rename(columns={0: 'id'}).merge(items).head(k)

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link.split('=')[1]
    return f'<a target="_blank" href="{link}">{text}</a>'


#If nightlife 
if venue_type == 'Nightlife': 
    venue = st.selectbox(
    'Pick a venue and we will make you recommendations', nightlife_df['name_and_location'])
    nightlife_df_subset = nightlife_df[nightlife_df['name_and_location'] == venue].reset_index(drop=True)
    id = nightlife_df_subset['id'].iloc[0]
    recs = genre_recommendations(i=id, M=nightlife_cosine_sim_df, items=nightlife_df, k=15)
    recs = recs[['name', 'url', 'review_count', 'rating', 'price', 'location.address1']]
# link is the column with hyperlinks
    recs['url'] = recs['url'].apply(make_clickable)
    recs = recs.to_html(escape=False)
    st.write(recs, unsafe_allow_html=True)

#If restaurant
if venue_type == 'Restaurants': 
    venue = st.selectbox(
    'Pick a venue and we will make you recommendations', restaurants_df['name_and_location'])
    restaurants_df_subset = restaurants_df[restaurants_df['name_and_location'] == venue].reset_index(drop=True)
    id = restaurants_df_subset['id'].iloc[0]
    recs = genre_recommendations(i=id, M=restaurant_cosine_sim_df, items=restaurants_df, k=15)
    recs = recs[['name', 'url', 'review_count', 'rating', 'price', 'location.address1']]
# link is the column with hyperlinks
    recs['url'] = recs['url'].apply(make_clickable)
    recs = recs.to_html(escape=False)
    st.write(recs, unsafe_allow_html=True)

#If coffee shop
if venue_type == 'Coffee Shops': 
    venue = st.selectbox(
    'Pick a venue and we will make you recommendations', coffee_df['name_and_location'])
    coffee_df_subset = coffee_df[coffee_df['name_and_location'] == venue].reset_index(drop=True)
    id = coffee_df_subset['id'].iloc[0]
    recs = genre_recommendations(i=id, M=coffee_cosine_sim_df, items=coffee_df, k=15)
    recs = recs[['name', 'url', 'review_count', 'rating', 'price', 'location.address1']]
# link is the column with hyperlinks
    recs['url'] = recs['url'].apply(make_clickable)
    recs = recs.to_html(escape=False)
    st.write(recs, unsafe_allow_html=True)


# option = st.selectbox('Pick one of your favorite places. We will find more just like it',
#                         )
# image = Image.open('images/pink_pin.jpg')
# st.image(image)
