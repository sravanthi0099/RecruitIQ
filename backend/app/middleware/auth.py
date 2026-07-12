"""Authentication middleware."""

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from loguru import logger

from app.config import settings

security = HTTPBearer()


async def verify_token(credentials: HTTPAuthCredentials) -> dict:
    """
    Verify JWT token.
    
    Args:
        credentials: HTTP bearer credentials
        
    Returns:
        dict: Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    try:
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except ExpiredSignatureError:
        logger.warning("Expired token attempted")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError as e:
        logger.warning(f"Invalid token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(credentials: HTTPAuthCredentials) -> dict:
    """
    Get current user from token.
    
    Args:
        credentials: HTTP bearer credentials
        
    Returns:
        dict: User information from token
    """
    payload = await verify_token(credentials)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return {"user_id": user_id, "payload": payload}