import unittest
from contextlib import redirect_stderr
from io import StringIO
import tempfile
from pathlib import Path

from SearchEngine import SearchEngine
from tests.helpers import make_document, reset_corpus


class SearchEngineTests(unittest.TestCase):
    def setUp(self):
        self.corpus = reset_corpus()
        self.corpus.add_document(
            make_document("Reddit", "Serve and tennis", "alice", "tennis serve court")
        )
        self.corpus.add_document(
            make_document("Arxiv", "Tennis analysis", "bob", "tennis tennis rally court")
        )
        self.corpus.add_document(
            make_document("Reddit", "Rally", "carol", "rally court")
        )
        with redirect_stderr(StringIO()):
            self.engine = SearchEngine(self.corpus)

    def test_search_ranks_best_match_and_returns_metadata(self):
        with redirect_stderr(StringIO()):
            results = self.engine.search("tennis", n=10)

        self.assertEqual(list(results["id"]), [1, 0])
        self.assertEqual(
            list(results.columns),
            ["id", "title", "author", "source", "date", "url", "score"],
        )
        self.assertTrue((results["score"] > 0).all())
        self.assertTrue(results["score"].is_monotonic_decreasing)

    def test_search_returns_empty_for_blank_unknown_and_corpus_wide_terms(self):
        with redirect_stderr(StringIO()):
            self.assertTrue(self.engine.search("", n=5).empty)
            self.assertTrue(self.engine.search("unknown", n=5).empty)
            self.assertTrue(self.engine.search("court", n=5).empty)

    def test_search_respects_result_limit(self):
        with redirect_stderr(StringIO()):
            results = self.engine.search("tennis", n=1)

        self.assertEqual(len(results), 1)
        self.assertEqual(results.iloc[0]["id"], 1)

    def test_empty_corpus_search_has_expected_columns(self):
        empty_corpus = reset_corpus("empty")
        with redirect_stderr(StringIO()):
            results = SearchEngine(empty_corpus).search("tennis", n=5)

        self.assertTrue(results.empty)
        self.assertEqual(
            list(results.columns),
            ["id", "title", "author", "source", "date", "url", "score"],
        )

    def test_complete_save_reload_search_and_context_workflow(self):
        corpus = reset_corpus("tennis")
        corpus.add_document(
            make_document(
                "Reddit",
                "Serve technique",
                "player_one",
                "A powerful tennis serve wins the point.",
            )
        )
        corpus.add_document(
            make_document(
                "Arxiv",
                "Tennis study",
                "researcher",
                "This study examines tennis match statistics.",
            )
        )

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "corpus.tsv"
            corpus.save(str(path))
            loaded_corpus = reset_corpus().load(str(path))

        with redirect_stderr(StringIO()):
            results = SearchEngine(loaded_corpus).search("serve tennis", n=5)
        passages = loaded_corpus.concorde("serve", size_context=20)

        self.assertEqual(loaded_corpus.name, "tennis")
        self.assertEqual(len(loaded_corpus.documents), 2)
        self.assertEqual(results.iloc[0]["title"], "Serve technique")
        self.assertIn("player_one", loaded_corpus.authors)
        self.assertEqual(len(passages), 1)
        self.assertEqual(passages.iloc[0]["expression"].lower(), "serve")


if __name__ == "__main__":
    unittest.main()
