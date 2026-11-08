from datetime import datetime, timezone

from Corpus import Corpus
from Document import DocumentFactory


def reset_corpus(name: str = "test") -> Corpus:
    corpus = Corpus(name=name)
    corpus.name = name
    corpus.documents.clear()
    corpus.id_document = 0
    corpus.authors.clear()
    corpus.concatenated_text = ""
    corpus.vocab = {}
    corpus.mat_TF = None
    corpus.mat_TFxIDF = None
    return corpus


def make_document(
    source: str,
    title: str,
    author: str,
    text: str,
):
    kwargs = {}
    if source == "Reddit":
        kwargs["num_comments"] = 3
    elif source == "Arxiv":
        kwargs["coauthors"] = ["Coauthor"]

    return DocumentFactory.create_document(
        source=source,
        title=title,
        author=author,
        date=datetime(2024, 1, 2, tzinfo=timezone.utc),
        url=f"https://example.test/{title.replace(' ', '-')}",
        text=text,
        **kwargs,
    )
