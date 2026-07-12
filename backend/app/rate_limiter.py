"""Shared rate limiter instance.

`slowapi` was already in requirements.txt but never actually wired up --
meaning every endpoint, including the LLM-calling ones (full-analysis,
interview evaluation, etc.), had no protection against being hammered.
This sets a global default limit (per client IP) that applies
automatically to every route once registered in main.py, with no need
to decorate each endpoint individually.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
)