import os
import pandas as pd
from Corpus import Corpus
from reddit_data import collect_reddit_posts
from arxiv_data import collect_arxiv_posts

if __name__ == "__main__":

    taille_docs = 10
    theme = "tennis"

    corpus_path = "corpus.csv"
    corpus = Corpus(name=theme)
    if os.path.exists(corpus_path):
        corpus.load(corpus_path)
    else:
        docs_reddit = collect_reddit_posts(taille_docs, theme)
        docs_arxiv = collect_arxiv_posts(taille_docs, theme)

        for doc in docs_reddit + docs_arxiv:
            corpus.add_document(doc)

    corpus.save(corpus_path)
    corpus.load(corpus_path)
    print(corpus)

    author_name = input("Nom de l'auteur : ").strip()
    if author_name in corpus.authors:
        author = corpus.authors[author_name]
        average_words = sum(
            len(doc.text.split()) for doc in author.production.values()
        ) / author.nb_docs
        print(f"{author.nb_docs} document(s)")
        print(f"Taille moyenne : {average_words:.2f} mots")
    else:
        print("Auteur introuvable")

    df = pd.DataFrame([
        {
            "id": document_id,
            "title": doc.title,
            "authors": doc.author,
            "source": doc.getType(),
            "date": doc.date,
            "url": doc.url,
            "text": doc.text,
        }
        for document_id, doc in corpus.documents.items()
    ])
    print(df)

    print(len(df))
    
    for articles in df['text']:
        print(f" le nomber de mots est {len(articles.split(' '))}")
        print(f" le nomber de phrases est {len(articles.split('.'))}")
    
    df = df[df["text"].str.len() >= 100]
    
    corpus = " ".join(df["text"])
    
    print(corpus)
