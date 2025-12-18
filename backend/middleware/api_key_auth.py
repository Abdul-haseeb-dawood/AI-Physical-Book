from fastapi import Request, HTTPException
from config.settings import settings
import os


async def api_key_auth(request: Request):
    """
    API key authentication middleware
    """
    # If no API key is configured, skip authentication
    if not settings.API_KEY:
        return  # Allow request to proceed without API key

    # Extract API key from header
    api_key = request.headers.get("X-API-Key")

    # Check if API key matches the expected value
    if not api_key or api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")