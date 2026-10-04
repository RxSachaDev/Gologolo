from dataclasses import dataclass

@dataclass
class Author:
    name: str
    nb_docs: int
    production: dict
