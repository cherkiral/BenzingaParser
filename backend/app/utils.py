from fastapi import HTTPException
from functools import wraps


def handle_exceptions(route_function):
    @wraps(route_function)
    async def wrapper(*args, **kwargs):
        try:
            return await route_function(*args, **kwargs)
        except Exception as e:
            # Add logging here if desired
            raise HTTPException(status_code=500, detail=str(e))

    return wrapper
