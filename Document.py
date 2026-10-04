from dataclasses import dataclass
from datetime import datetime

@dataclass
class Document:
    title: str
    authors: list[str]
    date: datetime
    url: str
    text: str
    origin: str

    def __str__(self):
        return f"Titre : {self.title}\n"