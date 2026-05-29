import uuid

import structlog

from .dependencies import get_user_repository

logger = structlog.get_logger(__name__)
MOCK_USER_ID: uuid.UUID | None = None

async def get_current_user_id() -> uuid.UUID:
    """
    Placeholder function to simulate user authentication and retrieval of the current user's ID.
    """
    global MOCK_USER_ID
    
    if MOCK_USER_ID is not None:
        logger.debug("auth.mock_user.cached", user_id=str(MOCK_USER_ID))
        return MOCK_USER_ID
    
    logger.info("auth.mock_user.fetch")
    MOCK_USER_ID = get_user_repository().get_all().first().id
    logger.info("auth.mock_user.assigned", user_id=str(MOCK_USER_ID))
    return MOCK_USER_ID