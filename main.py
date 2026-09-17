
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
        docs_reddit, origins_reddit = collect_reddit_posts(taille_docs)

        # Récupération ArXiv
        docs_arxiv, origins_arxiv = collect_arxiv_posts(taille_docs)

        # Fusion des deux sources
        docs = docs_reddit + docs_arxiv
        origins = origins_reddit + origins_arxiv

        # Création du DataFrame
        df = pd.DataFrame({
            "id": range(len(docs)),
            "text": docs,
            "origin": origins
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