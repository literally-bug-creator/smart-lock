import os

from database import get_session
from database.models import User
from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase


async def get_user_db(session=Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)


PASSWORD_SECRET = os.environ["PASSWORD_SECRET"]


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = PASSWORD_SECRET
    verification_token_secret = PASSWORD_SECRET


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy[User, int]:
    token_lifetime = os.getenv("JWT_EXPIRATION_TIME_SECONDS")
    if token_lifetime is not None:
        token_lifetime = int(token_lifetime)
    return JWTStrategy(secret=PASSWORD_SECRET, lifetime_seconds=token_lifetime)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_active_user_optional = fastapi_users.current_user(active=True, optional=True)
