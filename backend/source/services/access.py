from api.users import current_active_user
from fastapi import Depends, HTTPException, status
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from database.models import User


class AccessService:
    def __init__(
        self,
        user: "User" = Depends(current_active_user),
    ):
        pass

    async def read(self) -> None:  # TODO: Implement service logic
        ...