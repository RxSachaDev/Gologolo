import praw
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from Document import Document

load_dotenv()

def collect_reddit_posts(taille_docs: int, theme: str):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    subr = reddit.subreddit(theme)
    posts = list(subr.hot(limit=taille_docs))

    docs = []

    for post in posts:
        if post.selftext:
            title = post.title
            authors = [str(post.author)]
            date = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
            url = "https://www.reddit.com" + post.permalink
            text = post.selftext.replace("\n", " ")

            docs.append(
                Document(
                    title = title,
                    authors = authors,
                    date = date,
                    url = url,
                    text = text,
                    origin = "reddit"
                )
            )

    return docs