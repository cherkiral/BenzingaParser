from .models import LinkItem, ArticleItem
from .db import get_database


async def create_article_item(news_item: ArticleItem):
    db = await get_database()
    collection = db['articles']
    new_item = collection.insert_one(news_item.dict())
    return new_item.inserted_id


async def get_all_articles():
    db = await get_database()
    news_collection = db['articles']
    news_items = news_collection.find({})
    return [ArticleItem(**item) for item in news_items]


async def create_link_item(news_item: LinkItem):
    db = await get_database()
    collection = db['links']
    new_item = collection.insert_one(news_item.dict())
    return new_item.inserted_id


async def get_all_links():
    db = await get_database()
    news_collection = db['links']
    news_items = news_collection.find({})
    return [LinkItem(**item) for item in news_items]
