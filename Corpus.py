from dataclasses import dataclass
from Document import Document
from Author import Author

@dataclass
class Corpus:
    name: str
    documents: dict[int, Document] 
    id_document: int = 0
    authors: dict[str, Author]

    def add_document(self, doc: Document) -> None:
        document_id = self.id_document
        self.documents[document_id] = doc
        self.id_document += 1

        for author_name in dict.fromkeys(doc.authors):
            if author_name not in self.authors:
                self.authors[author_name] = Author(
                    name=author_name,
                    nb_docs=0,
                    production={}
                )
            self.authors[author_name].add(doc)

