from dataclasses import dataclass
from Document import Document
from Author import Author

@dataclass
class Corpus:
    name: str
    documents: dict[int, Document]
    id_documents: int
    authors: dict[int, Author]

