"""
LiteTokenRepository 实现

使用 JSON 文件存储普通用户 Token，保证并发安全
"""

from __future__ import annotations

import json
import os
import secrets
from datetime import datetime, timedelta
from typing import List, Optional

from filelock import FileLock

from .interfaces import TokenRepository, TokenInfo, TokenStatus


class LiteTokenRepository(TokenRepository):
    """基于 JSON 文件的 Token 存储库"""

    def __init__(self, storage_path: str, lock_path: Optional[str] = None):
        self.storage_path = storage_path
        self.lock_path = lock_path or f"{storage_path}.lock"

        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        if not os.path.exists(storage_path):
            with open(storage_path, "w", encoding="utf-8") as f:
                json.dump({"tokens": []}, f)

    def _load_tokens(self) -> List[TokenInfo]:
        with FileLock(self.lock_path):
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [TokenInfo(**token) for token in data.get("tokens", [])]

    def _save_tokens(self, tokens: List[TokenInfo]) -> None:
        with FileLock(self.lock_path):
            data = {"tokens": [token.dict() for token in tokens]}
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)

    def _generate_token(self) -> str:
        return secrets.token_urlsafe(24)

    def create_user_token(
        self,
        label: str,
        scopes: List[str],
        created_by: str,
        expires_in_hours: Optional[int] = None,
    ) -> TokenInfo:
        token_info = TokenInfo(
            token=self._generate_token(),
            label=label,
            scopes=scopes,
            status=TokenStatus.ACTIVE,
            created_at=datetime.utcnow(),
            last_used_at=None,
            expires_at=(datetime.utcnow() + timedelta(hours=expires_in_hours))
            if expires_in_hours
            else None,
        )

        tokens = self._load_tokens()
        tokens.append(token_info)
        self._save_tokens(tokens)
        return token_info

    def revoke_token(self, token: str) -> bool:
        tokens = self._load_tokens()
        updated = False

        for t in tokens:
            if t.token == token:
                t.status = TokenStatus.REVOKED
                updated = True
                break

        if updated:
            self._save_tokens(tokens)
        return updated

    def validate_token(self, token: str) -> Optional[TokenInfo]:
        tokens = self._load_tokens()
        for t in tokens:
            if t.token == token:
                if t.status != TokenStatus.ACTIVE:
                    return None
                if t.expires_at and datetime.utcnow() > t.expires_at:
                    return None
                return t
        return None

    def list_tokens(
        self,
        status: Optional[TokenStatus] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> List[TokenInfo]:
        tokens = self._load_tokens()

        if status:
            tokens = [t for t in tokens if t.status == status]

        tokens.sort(key=lambda t: t.created_at, reverse=True)

        start = (page - 1) * page_size
        end = start + page_size
        return tokens[start:end]

    def update_last_used(self, token: str) -> None:
        tokens = self._load_tokens()
        updated = False

        for t in tokens:
            if t.token == token:
                t.last_used_at = datetime.utcnow()
                updated = True
                break

        if updated:
            self._save_tokens(tokens)
