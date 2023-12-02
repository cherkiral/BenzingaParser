from pydantic import BaseModel

class LinkItem(BaseModel):
    link: str
    title: str

class ArticleItem(BaseModel):
    title: str
    content: str