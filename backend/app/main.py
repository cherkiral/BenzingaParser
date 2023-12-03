from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

from .routes import router as news_router

app = FastAPI()

app.include_router(news_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)