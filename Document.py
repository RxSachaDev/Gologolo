from dataclasses import dataclass

@dataclass
class Document:
    title: str
    authors: list
    date: str
    url: str
    text: str

    def __str__(self):
        return f"Titre : {self.title}\n"