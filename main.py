
from reddit_data import *
from arxiv_data import *
import pandas as pd

if __name__ == "__main__":

    taille_docs = 10

    if (os.path.exists("corpus.csv")):
        df = pd.read_csv("corpus.csv", sep="\t")
        print(df)
    else:

        # Récupération Reddit
        docs_reddit = collect_reddit_posts(taille_docs)

        # Récupération ArXiv
        docs_arxiv = collect_arxiv_posts(taille_docs)

        # Fusion des deux sources
        docs = docs_reddit + docs_arxiv

        # Création du DataFrame
        df = pd.DataFrame({
            "id": range(len(docs)),
            "title": [doc["title"] for doc in docs],
            "authors": [doc["authors"] for doc in docs],
            "date": [doc["date"] for doc in docs],
            "url": [doc["url"] for doc in docs],
            "text": [doc["text"] for doc in docs],
            "origin": [doc["origin"] for doc in docs]
        })

        # Sauvegarde
        df.to_csv("corpus.csv", sep="\t", index=False)

        print(df)

    print(len(df))
    
    for articles in df['text']:
        print(f" le nomber de mots est {len(articles.split(' '))}")
        print(f" le nomber de phrases est {len(articles.split('.'))}")
    
    df = df[df["text"].str.len() >= 100]
    
    corpus = " ".join(df["text"])
    
    print(corpus)