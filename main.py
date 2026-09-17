
from Script import *


if __name__ == "__main__":
    if os.path.exists('articles_reddit.csv'):
        df = catch_reddit_csv()
    else:
        df = collect_reddit_posts(taille_docs)

    print(len(df))

    for articles in df['text']:
        print(f" le nomber de mots est {len(articles.split(' '))}")
        print(f" le nomber de phrases est {len(articles.split('.'))}")