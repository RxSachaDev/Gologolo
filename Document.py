from dataclasses import dataclass
from datetime import datetime

@dataclass
class Document:
    title: str
    authors: str
    date: datetime
    url: str
    text: str
    origin: str

    def __str__(self):
        return f"Titre : {self.title}\n"


class RedditDocument(Document):
    def __init__(
        self, title: str, authors: str, date: datetime, url: str, text: str, origin: str, num_comments: int) -> None:
        super().__init__(title, authors, date, url, text, origin)
        self.num_comments = num_comments

    def get_num_comments(self) -> int:
        return self.num_comments

    def set_num_comments(self, num_comments: int) -> None:
        self.num_comments = num_comments

    def __str__(self) -> str:
        return (
            f"{super().__str__()}"
            f"Nombre de commentaires : {self.num_comments}\n"
        )