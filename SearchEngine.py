from collections import Counter
from math import log, sqrt

import pandas as pd
from scipy.sparse import csr_matrix

from Corpus import Corpus
from tools.text import clean_text

class SearchEngine:
    def __init__(self, corpus: Corpus) -> None:
        self.corpus = corpus
        self.corpus._build_term_matrices()

    def search(self, mots_clefs: str, n: int) -> pd.DataFrame:
        columns = ["id", "title", "author", "source", "date", "url", "score"]
        word_frequencies = Counter(clean_text(mots_clefs).split())
        if not word_frequencies or not self.corpus.documents:
            return pd.DataFrame(columns=columns)

        if self.corpus.mat_TF is None or self.corpus.mat_TFxIDF is None:
            self.corpus._build_term_matrices()

        query_word_ids = []
        query_weights = []
        for word, count in word_frequencies.items():
            if word not in self.corpus.vocab:
                continue

            word_data = self.corpus.vocab[word]
            query_word_ids.append(word_data["id"])
            query_weights.append(
                count * log(len(self.corpus.documents) / word_data["DF"])
            )

        if not query_word_ids:
            return pd.DataFrame(columns=columns)

        query_vector = csr_matrix(
            (
                query_weights,
                ([0] * len(query_word_ids), query_word_ids),
            ),
            shape=(1, len(self.corpus.vocab)),
        )
        query_norm = sqrt(float(query_vector.multiply(query_vector).sum()))
        if query_norm == 0:
            return pd.DataFrame(columns=columns)

        document_norms = (
            self.corpus.mat_TFxIDF.multiply(self.corpus.mat_TFxIDF)
            .sum(axis=1)
            .A1
        ) ** 0.5
        dot_products = (
            self.corpus.mat_TFxIDF @ query_vector.T
        ).toarray().ravel()

        rows = [
            {
                "id": document_id,
                "title": document.title,
                "author": document.author,
                "source": document.getType(),
                "date": document.date,
                "url": document.url,
                "score": float(dot_products[row] / (
                    document_norms[row] * query_norm
                )),
            }
            for row, (document_id, document) in enumerate(
                self.corpus.documents.items()
            )
            if document_norms[row] > 0 and dot_products[row] > 0
        ]
        results = pd.DataFrame(rows, columns=columns)
        return (
            results.sort_values(
                by=["score", "id"],
                ascending=[False, True],
            )
            .head(max(0, n))
            .reset_index(drop=True)
        )