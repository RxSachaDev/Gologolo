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

