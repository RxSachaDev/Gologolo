import praw
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from Document import DocumentFactory

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
            author = str(post.author)
            date = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
            url = "https://www.reddit.com" + post.permalink
            text = post.selftext.replace("\n", " ")

            docs.append(
                DocumentFactory.create_document(
                    source="Reddit",
                    title = title,
                    author = author,
                    date = date,
                    url = url,
                    text = text,
                    num_comments = post.num_comments
                )
            )

    return docs