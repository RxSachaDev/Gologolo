import praw
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

taille_docs=20

def collect_reddit_posts(taille_docs: int):
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
    return df

def catch_reddit_csv():
    ## Récupération du CSV des posts Reddit

    if os.path.exists('articles_reddit.csv'):
        df = pd.read_csv('articles_reddit.csv', sep='\t')
        print("CSV des posts Reddit récupéré avec succès.")
        return df
    else:
        print("Le fichier articles_reddit.csv n'existe pas. Veuillez d'abord collecter les posts Reddit.")
        return None