"""
FastAPI 依赖项定义
"""

from fastapi import Depends, HTTPException, status

from ..storage.interfaces import TokenRepository, TokenInfo


class UserContext:
    def __init__(self, token_info: TokenInfo):
        self.token_info = token_info


def get_current_user(token: str = Depends(...), repo: TokenRepository = Depends(...)) -> UserContext:
    token_info = repo.validate_token(token)
    if not token_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    repo.update_last_used(token)
    return UserContext(token_info)
