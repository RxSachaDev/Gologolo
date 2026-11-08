import unittest
from datetime import datetime

from Author import Author
from Document import ArxivDocument, Document, DocumentFactory, RedditDocument
from tools.text import clean_text


class DocumentTests(unittest.TestCase):
    def setUp(self):
        self.date = datetime(2024, 1, 2)

    def test_factory_creates_reddit_document_with_comments(self):
        document = DocumentFactory.create_document(
            "Reddit", "Match", "alice", self.date, "https://example.test/1",
            "A tennis match", num_comments=7,
        )

        self.assertIsInstance(document, RedditDocument)
        self.assertIsInstance(document, Document)
        self.assertEqual(document.getType(), "Reddit")
        self.assertEqual(document.get_num_comments(), 7)

    def test_factory_creates_arxiv_document_with_coauthors(self):
        document = DocumentFactory.create_document(
            "Arxiv", "Study", "alice", self.date, "https://example.test/2",
            "A tennis study", coauthors=["bob"],
        )

        self.assertIsInstance(document, ArxivDocument)
        self.assertEqual(document.getType(), "Arxiv")
        self.assertEqual(document.get_coauthors(), ["bob"])

    def test_factory_rejects_missing_source_specific_metadata(self):
        common = ("title", "author", self.date, "https://example.test", "text")

        with self.assertRaisesRegex(ValueError, "num_comments est requis"):
            DocumentFactory.create_document("Reddit", *common)
        with self.assertRaisesRegex(ValueError, "coauthors est requis"):
            DocumentFactory.create_document("Arxiv", *common)
        with self.assertRaisesRegex(ValueError, "Source de document inconnue"):
            DocumentFactory.create_document("Other", *common)

    def test_author_tracks_its_production(self):
        first = Document("First", "alice", self.date, "url1", "text")
        second = Document("Second", "alice", self.date, "url2", "text")
        author = Author("alice", 0, {})

        author.add(first)
        author.add(second)

        self.assertEqual(author.nb_docs, 2)
        self.assertEqual(author.production, {0: first, 1: second})

    def test_clean_text_normalizes_case_punctuation_and_whitespace(self):
        self.assertEqual(clean_text("Tennis,\nACE! 2024"), "tennis ace")


if __name__ == "__main__":
    unittest.main()
