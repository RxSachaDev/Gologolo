from dataclasses import dataclass
from datetime import datetime

@dataclass
class Document:
    title: str
    author: str
    date: datetime
    url: str
    text: str
    type: str = "Document"

    def __str__(self):
        return f"Titre : {self.title}\n"


class RedditDocument(Document):
    def __init__(
        self, title: str, author: str, date: datetime, url: str, text: str, num_comments: int) -> None:
        super().__init__(title, author, date, url, text, "Reddit")
        self.num_comments = num_comments

    def getType(self) -> str:
        return self.type

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
        super().__init__(title, author, date, url, text, "Arxiv")
        self.coauthors = coauthors

    def getType(self) -> str:
        return self.type

    def get_coauthors(self) -> list[str]:
        return self.coauthors

    def set_coauthors(self, coauthors: list[str]) -> None:
        self.coauthors = coauthors

    def __str__(self) -> str:
        coauthors = ", ".join(self.coauthors)
        return f"{super().__str__()}Coauteurs : {coauthors}\n"


class DocumentFactory:
    @staticmethod
    def create_document(source: str, title: str, author: str, date: datetime, url: str, text: str, *, num_comments: int | None = None, coauthors: list[str] | None = None,) -> Document:
        if source == "Reddit":
            if num_comments is None:
                raise ValueError("num_comments est requis pour un document Reddit")
            return RedditDocument(
                title, author, date, url, text, num_comments
            )

        if source == "Arxiv":
            if coauthors is None:
                raise ValueError("coauthors est requis pour un document Arxiv")
            return ArxivDocument(title, author, date, url, text, coauthors)

        raise ValueError(f"Source de document inconnue : {source}")