import ast
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from math import log
from pathlib import Path

import pandas as pd
from scipy.sparse import csr_matrix, diags

from tools.text import clean_text

from Document import Document, DocumentFactory
from Author import Author


def singleton(cls):
    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper


@singleton
@dataclass
class Corpus:
    name: str
    documents: dict[int, Document] = field(default_factory=dict)
    id_document: int = 0
    authors: dict[str, Author] = field(default_factory=dict)
    concatenated_text: str = ""
    vocab: dict[str, dict[str, int]] = field(default_factory=dict)
    mat_TF: csr_matrix | None = None
    mat_TFxIDF: csr_matrix | None = None

    def add_document(self, doc: Document) -> None:
        document_id = self.id_document
        self.documents[document_id] = doc
        self.id_document += 1
        self.concatenated_text = ""
        self.vocab = {}
        self.mat_TF = None
        self.mat_TFxIDF = None

        self._add_document_to_authors(doc)

    def _add_document_to_authors(self, doc: Document) -> None:
        if doc.author not in self.authors:
            self.authors[doc.author] = Author(
                name=doc.author,
                nb_docs=0,
                production={}
            )
        self.authors[doc.author].add(doc)

    def save(self, path: str = "corpus.csv") -> None:
        """Enregistre le corpus en TSV, avec les champs propres à chaque source."""
        rows = [
            {
                "corpus_name": self.name,
                "concatenated_text": (
                    self.concatenated_text if index == 0 else None
                ),
                "id": document_id,
                "title": doc.title,
                "author": doc.author,
                "type": doc.getType(),
                "date": doc.date.isoformat(),
                "url": doc.url,
                "text": doc.text,
                "num_comments": getattr(doc, "num_comments", None),
                "coauthors": repr(getattr(doc, "coauthors", [])),
            }
            for index, (document_id, doc) in enumerate(self.documents.items())
        ]
        if not rows:
            rows.append({
                "corpus_name": self.name,
                "concatenated_text": self.concatenated_text,
            })

        pd.DataFrame(rows).to_csv(path, sep="\t", index=False)

    def load(self, path: str = "corpus.csv") -> "Corpus":
        """Reconstruit les documents et les auteurs depuis un fichier TSV."""
        df = pd.read_csv(path, sep="\t")
        if "corpus_name" in df.columns and not df["corpus_name"].dropna().empty:
            corpus_name = str(df["corpus_name"].dropna().iloc[0])
        else:
            corpus_name = Path(path).stem

        self.name = corpus_name
        self.documents.clear()
        self.id_document = 0
        self.authors.clear()
        self.concatenated_text = ""
        self.vocab = {}
        self.mat_TF = None
        self.mat_TFxIDF = None
        if "concatenated_text" in df.columns:
            saved_text = df["concatenated_text"].dropna()
            if not saved_text.empty:
                self.concatenated_text = str(saved_text.iloc[0])
        for row in df.to_dict(orient="records"):
            if pd.isna(row.get("id")):
                continue

            if row["type"] == "Reddit":
                num_comments = row.get("num_comments", 0)
                if pd.isna(num_comments):
                    num_comments = 0
                doc = DocumentFactory.create_document(
                    source="Reddit",
                    title=row["title"],
                    author=row["author"],
                    date=datetime.fromisoformat(row["date"]),
                    url=row["url"],
                    text=row["text"],
                    num_comments=int(num_comments),
                )
            elif row["type"] == "Arxiv":
                coauthors_value = row.get("coauthors", "[]")
                if not isinstance(coauthors_value, str) or pd.isna(coauthors_value):
                    coauthors = []
                else:
                    coauthors = ast.literal_eval(coauthors_value)
                doc = DocumentFactory.create_document(
                    source="Arxiv",
                    title=row["title"],
                    author=row["author"],
                    date=datetime.fromisoformat(row["date"]),
                    url=row["url"],
                    text=row["text"],
                    coauthors=coauthors,
                )
            else:
                doc = DocumentFactory.create_document(
                    source=row["type"],
                    title=row["title"],
                    author=row["author"],
                    date=datetime.fromisoformat(row["date"]),
                    url=row["url"],
                    text=row["text"],
                )
            
            document_id = int(row["id"])
            self.documents[document_id] = doc
            self.id_document = max(self.id_document, document_id + 1)
            self._add_document_to_authors(doc)

        return self

    def display_documents_date_sorted(self, number: int) -> None:
        docs_sorted = sorted(
            self.documents.values(),
            key=lambda doc: doc.date,
            reverse=True
        )
        for doc in docs_sorted[:max(0, number)]:
            print(f"{doc.date} - {doc.title} [{doc.getType()}]")

    def display_documents_title_sorted(self, number: int) -> None:
        docs_sorted = sorted(
            self.documents.values(),
            key=lambda doc: doc.title.casefold()
        )
        for doc in docs_sorted[:max(0, number)]:
            print(f"{doc.title} - {doc.date} [{doc.getType()}]")

    def __repr__(self) -> str:
        return (
            f"Corpus(name={self.name}, documents={len(self.documents)}, "
            f"authors={len(self.authors)})"
        )

    def search(self, keyword: str) -> list[str]:
        if keyword == "":
          return []        
          
        if self.concatenated_text == "":
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
                for document_id, doc in self.documents.items()
            ])

            self.concatenated_text = " ".join(df["text"])

        return re.findall(r"[^.]*\b" + keyword + r"\b[^.]*", self.concatenated_text, re.IGNORECASE)

    def concorde(self, keyword: str, size_context: int) -> list[str]:
        if self.concatenated_text == "":
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
                for document_id, doc in self.documents.items()
            ])
        
            self.concatenated_text = " ".join(df["text"])

        resultats = re.findall(
            r"(.{0," + str(size_context) + r"})"
            + r"(" + re.escape(keyword) + r")"
            + r"(.{0," + str(size_context) + r"})",
            self.concatenated_text,
            re.IGNORECASE
        )

        return pd.DataFrame(resultats, columns=["contexte gauche", "expression", "contexte droit"])

    def _build_term_matrices(self) -> None:
        # Une ligne représente un document et une colonne un terme du vocabulaire.
        document_term_frequencies = []
        vocabulary_words = set()

        for doc in self.documents.values():
            term_frequencies = Counter(clean_text(doc.text).split())
            document_term_frequencies.append(term_frequencies)
            vocabulary_words.update(term_frequencies)

        self.vocab = {
            word: {
                "id": identifier,
                "TF": 0,
                "DF": 0,
            }
            for identifier, word in enumerate(sorted(vocabulary_words))
        }

        rows = []
        columns = []
        values = []

        word_ids = {
            word: details["id"]
            for word, details in self.vocab.items()
        }
        for document_id, term_frequencies in enumerate(document_term_frequencies):
            for word, count in term_frequencies.items():
                rows.append(document_id)
                columns.append(word_ids[word])
                values.append(count)

        self.mat_TF = csr_matrix(
            (values, (rows, columns)),
            shape=(len(self.documents), len(self.vocab)),
            dtype=int,
        )

        total_occurrences = self.mat_TF.sum(axis=0).A1
        document_counts = self.mat_TF.getnnz(axis=0)
        document_count = len(self.documents)
        for word, details in self.vocab.items():
            word_id = details["id"]
            details["TF"] = int(total_occurrences[word_id])
            details["DF"] = int(document_counts[word_id])

        idf_values = [
            # Un terme partagé par tous les documents reçoit un poids IDF nul.
            log(document_count / document_counts[word_id])
            for word_id in range(len(self.vocab))
        ]
        self.mat_TFxIDF = (
            self.mat_TF @ diags(idf_values, format="csr")
        ).tocsr()

    def stats(self) -> None:
        self._build_term_matrices()
        freq = pd.DataFrame.from_dict(
            self.vocab,
            orient="index",
            columns=["id", "TF", "DF"],
        )
        freq.index.name = "mot"

        print("Nombre de mots différents :", len(self.vocab))
        print(freq.sort_values(by="TF", ascending=False).head(10))