import os
import pandas as pd
from Document import Document
from reddit_data import collect_reddit_posts
from arxiv_data import collect_arxiv_posts

if __name__ == "__main__":

    taille_docs = 10
    theme = "tennis"

    if (os.path.exists("corpus.csv")):
        df = pd.read_csv("corpus.csv", sep="\t")
        print(df)
    else:

        # Récupération Reddit
        docs_reddit = collect_reddit_posts(taille_docs, theme)

        # Récupération ArXiv
        docs_arxiv = collect_arxiv_posts(taille_docs, theme)

        # Fusion des deux sources
        all_docs: list[Document] = docs_reddit + docs_arxiv

        documents = {i: doc for i, doc in enumerate(all_docs)}

        # Création du DataFrame
        df = pd.DataFrame([
            {
                "id": document_id,
                "title": doc.title,
                "authors": doc.authors,
                "date": doc.date,
                "url": doc.url,
                "text": doc.text,
                "origin": doc.origin
            }
            for document_id, doc in documents.items()
        ])

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