"""Shared auth: bearer token between Next.js and this service."""

import logging
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

log = logging.getLogger('gymfreek-ai')
_optional_bearer = HTTPBearer(auto_error=False)
_warned = False


def _expected() -> str:
    return os.environ.get('AI_SERVICE_TOKEN', '')


async def require_service_token(
    creds: HTTPAuthorizationCredentials | None = Depends(_optional_bearer),
) -> None:
    expected = _expected()
    if not expected:
        global _warned
        if not _warned:
            log.warning('AI_SERVICE_TOKEN unset - accepting unauthenticated calls (dev only).')
            _warned = True
        return
    if creds is None or creds.scheme.lower() != 'bearer' or creds.credentials != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Bad service token.')
