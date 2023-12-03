from typing import List
from . import crud
from fastapi import APIRouter, Body
from .models import LinkItem, ArticleItem
from .parser.scraper import parse_and_sort, parse_article_content, parse_last_article_on_page
from .utils import handle_exceptions
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/links", response_model=List[LinkItem])
@handle_exceptions
async def get_links(limit: int = 10):
    return await crud.get_links(limit)


@router.get("/parse_links", response_model=List[LinkItem])
@handle_exceptions
async def parse_links(limit: int = 10):
    last_article = await parse_last_article_on_page()

    new_links = await parse_and_sort(f'https://www.benzinga.com/api/news?channels=2&limit={limit}&last={last_article}')

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
