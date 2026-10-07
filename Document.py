from dataclasses import dataclass
from datetime import datetime

@dataclass
class Document:
    title: str
    author: str
    date: datetime
    url: str
    text: str

    def __str__(self):
        return f"Titre : {self.title}\n"


class RedditDocument(Document):
    def __init__(
        self, title: str, author: str, date: datetime, url: str, text: str, num_comments: int) -> None:
        super().__init__(title, author, date, url, text)
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


class ArxivDocument(Document):
    def __init__(
        self, title: str, author: str, date: datetime, url: str, text: str, coauthors: list[str],
    ) -> None:
        super().__init__(title, author, date, url, text)
        self.coauthors = coauthors

    def get_coauthors(self) -> list[str]:
        return self.coauthors

    def set_coauthors(self, coauthors: list[str]) -> None:
        self.coauthors = coauthors

    def __str__(self) -> str:
        coauthors = ", ".join(self.coauthors)
        return f"{super().__str__()}Coauteurs : {coauthors}\n"