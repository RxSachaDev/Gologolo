import praw
import urllib.request
import xmltodict
import json
import pickle
import datetime
import pandas as pd
import os

taille_docs=20

## Récupération de textes depuis Reddit

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

subr = reddit.subreddit('tennis')

posts = list(subr.hot(limit=taille_docs))

docs = []
origins = []

for post in posts:

    if post.selftext:
        texte = post.selftext.replace("\n", " ")
        docs.append(texte)
        origins.append("reddit")

print("Nombre de posts Reddit collectés :", len(docs))


## Création du DataFrame

df = pd.DataFrame({
    "id": range(len(docs)),
    "text": docs,
    "origin": origins
})

df.to_csv('articles_reddit.csv', sep='\t', index=False)

print(df)