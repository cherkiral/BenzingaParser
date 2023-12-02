from typing import List
from . import crud
from fastapi import APIRouter, Body
from .models import LinkItem, ArticleItem
from .parser.scraper import parse_and_sort, parse_article_content
from .utils import handle_exceptions

router = APIRouter()


# @router.get("/articles", response_model=List[ArticleItem])
# @handle_exceptions
# async def get_all_articles():
#     return await crud.get_all_articles()
#
#
# @router.post("/articles", response_model=ArticleItem)
# @handle_exceptions
# async def add_articles_item(articles_item: ArticleItem = Body(...)):
#     return await crud.create_article_item(articles_item)
#
#
# @router.get("/links", response_model=List[LinkItem])
# @handle_exceptions
# async def get_all_links():
#     return await crud.get_all_links()
#
#
# @router.post("/links", response_model=LinkItem)
# @handle_exceptions
# async def add_links_item(link_item: LinkItem = Body(...)):
#     return await crud.create_link_item(link_item)


@router.get("/parse_links", response_model=List[LinkItem])
@handle_exceptions
async def parse_links(limit: int = 10):
    new_links = await parse_and_sort(f'https://www.benzinga.com/api/news?channels=2&limit={limit}')

    existing_links = await crud.get_all_links()

    existing_urls = {link.link for link in existing_links}

    unique_links = [link for link in new_links if link['link'] not in existing_urls]

    for link in unique_links:
        link_item = LinkItem(**link)
        await crud.create_link_item(link_item)

    return unique_links


@router.get("/parse_article", response_model=ArticleItem)
@handle_exceptions
async def parse_article(article_url: str):
    article = await parse_article_content(article_url)
    return ArticleItem(**article)
