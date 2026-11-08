import tempfile
import unittest
from pathlib import Path

from tests.helpers import make_document, reset_corpus


class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.corpus = reset_corpus()
        self.corpus.add_document(
            make_document("Reddit", "Serve tips", "alice", "Tennis serve.")
        )
        self.corpus.add_document(
            make_document("Arxiv", "Tennis study", "bob", "Tennis rally.")
        )

    def test_add_document_assigns_ids_and_groups_authors(self):
        self.corpus.add_document(
            make_document("Reddit", "Second post", "alice", "Rally.")
        )

        self.assertEqual(list(self.corpus.documents), [0, 1, 2])
        self.assertEqual(self.corpus.authors["alice"].nb_docs, 2)
        self.assertEqual(len(self.corpus.authors["bob"].production), 1)

    def test_add_document_invalidates_term_matrices(self):
        self.corpus._build_term_matrices()
        self.assertIsNotNone(self.corpus.mat_TF)

        self.corpus.add_document(
            make_document("Reddit", "Another post", "alice", "Ace.")
        )

        self.assertIsNone(self.corpus.mat_TF)
        self.assertIsNone(self.corpus.mat_TFxIDF)
        self.assertEqual(self.corpus.vocab, {})

    def test_term_statistics_count_frequency_and_document_frequency(self):
        self.corpus._build_term_matrices()

        self.assertEqual(self.corpus.vocab["tennis"]["TF"], 2)
        self.assertEqual(self.corpus.vocab["tennis"]["DF"], 2)
        self.assertEqual(self.corpus.vocab["serve"]["TF"], 1)
        self.assertEqual(self.corpus.vocab["serve"]["DF"], 1)

    def test_search_returns_matching_text_and_empty_for_empty_query(self):
        matches = self.corpus.search("tennis")

        self.assertEqual(len(matches), 2)
        self.assertTrue(all("tennis" in text.lower() for text in matches))
        self.assertEqual(self.corpus.search(""), [])

    def test_concorde_returns_context_dataframe(self):
        passages = self.corpus.concorde("serve", size_context=6)

        self.assertEqual(
            list(passages.columns),
            ["contexte gauche", "expression", "contexte droit"],
        )
        self.assertEqual(len(passages), 1)
        self.assertTrue((passages["expression"].str.lower() == "serve").all())
        self.assertTrue(
            all(len(context) <= 6 for context in passages["contexte gauche"])
        )
        self.assertTrue(
            all(len(context) <= 6 for context in passages["contexte droit"])
        )

    def test_save_and_load_preserve_source_specific_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "corpus.tsv"
            self.corpus.save(str(path))
            loaded = reset_corpus("to be replaced").load(str(path))

        self.assertEqual(loaded.name, "test")
        self.assertEqual(len(loaded.documents), 2)
        self.assertEqual(loaded.documents[0].get_num_comments(), 3)
        self.assertEqual(loaded.documents[1].get_coauthors(), ["Coauthor"])
        self.assertEqual(loaded.authors["alice"].nb_docs, 1)


if __name__ == "__main__":
    unittest.main()
