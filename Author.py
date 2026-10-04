from dataclasses import dataclass

@dataclass
class Document:
    name: str
    nb_docs: int
    production: dict
