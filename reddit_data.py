import praw
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def collect_reddit_posts(taille_docs: int):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    subr = reddit.subreddit("tennis")
    posts = list(subr.hot(limit=taille_docs))

    docs = []

    for post in posts:
        if post.selftext:
            title = post.title
            author = str(post.author)
            date = post.created_utc
            url = "https://www.reddit.com" + post.permalink
            text = post.selftext.replace("\n", " ")

            docs.append({
                "title": title,
                "authors": [author],
                "date": date,
                "url": url,
                "text": text,
                "origin" : "reddit"
            })

    return docs