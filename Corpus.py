import ast
from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd

from Document import Document
from Author import Author

@dataclass
class Corpus:
    name: str
    documents: dict[int, Document] = field(default_factory=dict)
    id_document: int = 0
    authors: dict[str, Author] = field(default_factory=dict)

    def add_document(self, doc: Document) -> None:
        document_id = self.id_document
        self.documents[document_id] = doc
        self.id_document += 1

        self._add_document_to_authors(doc)

    def _add_document_to_authors(self, doc: Document) -> None:
        for author_name in dict.fromkeys(doc.authors):
            if author_name not in self.authors:
                self.authors[author_name] = Author(
                    name=author_name,
                    nb_docs=0,
                    production={}
                )
            self.authors[author_name].add(doc)

    def save(self, path: str = "corpus.csv") -> None:
        rows = [
            {
                "corpus_name": self.name,
                "id": document_id,
                "title": doc.title,
                "authors": repr(doc.authors),
                "date": doc.date.isoformat(),
                "url": doc.url,
                "text": doc.text,
                "origin": doc.origin,
            }
            for document_id, doc in self.documents.items()
        ]
        if not rows:
            rows.append({"corpus_name": self.name})

        pd.DataFrame(rows).to_csv(path, sep="\t", index=False)

    @classmethod
    def load(cls, path: str = "corpus.csv") -> "Corpus":
        df = pd.read_csv(path, sep="\t")
        if "corpus_name" not in df.columns or df["corpus_name"].dropna().empty:
            raise ValueError("Le fichier ne contient pas le nom du corpus.")

        corpus = cls(name=str(df["corpus_name"].dropna().iloc[0]))
        for row in df.to_dict(orient="records"):
            if pd.isna(row.get("id")):
                continue

            authors = ast.literal_eval(row["authors"])
            doc = Document(
                title=row["title"],
                authors=authors,
                date=datetime.fromisoformat(row["date"]),
                url=row["url"],
                text=row["text"],
                origin=row["origin"],
            )
            document_id = int(row["id"])
            corpus.documents[document_id] = doc
            corpus.id_document = max(corpus.id_document, document_id + 1)
            corpus._add_document_to_authors(doc)

        return corpus

    def display_documents_date_sorted(self, number: int) -> None:
        docs_sorted = sorted(
            self.documents.values(),
            key=lambda doc: doc.date,
            reverse=True
        )
        for doc in docs_sorted[:max(0, number)]:
            print(f"{doc.date} - {doc.title}")

    def display_documents_title_sorted(self, number: int) -> None:
        docs_sorted = sorted(
            self.documents.values(),
            key=lambda doc: doc.title.casefold()
        )
        for doc in docs_sorted[:max(0, number)]:
            print(f"{doc.title} - {doc.date}")

    def __repr__(self) -> str:
        return (
            f"Corpus(name={self.name}, documents={len(self.documents)}, "
            f"authors={len(self.authors)})"
        )

