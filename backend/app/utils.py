from fastapi import HTTPException
from functools import wraps
import logging

logger = logging.getLogger(__name__)


def handle_exceptions(route_function):
    @wraps(route_function)
    async def wrapper(*args, **kwargs):
        try:
            return await route_function(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return wrapper
