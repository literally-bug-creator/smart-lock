from fastapi_users import schemas


class UserCreate(schemas.BaseUserCreate):
    ...


class UserRead(schemas.BaseUser[int]):
    ...


class UserUpdate(schemas.BaseUserUpdate):
    ...
