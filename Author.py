from dataclasses import dataclass
from Document import Document

@dataclass
class Author:
    name: str
    nb_docs: int
    production: dict[int, Document]

    def __str__(self) -> str:
        return f"Auteur : {self.name} ({self.nb_docs} document(s))"

    def add(self, doc: Document):
        document_id = len(self.production)
        self.production[document_id] = doc
        self.nb_docs += 1
