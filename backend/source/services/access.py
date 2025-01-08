from typing import TYPE_CHECKING

from fastapi import Depends, HTTPException, status

if TYPE_CHECKING:
    from database.models import User


class AccessService:
    def __init__(
        self,
    ):
        pass

    async def read(self) -> None:  # TODO: Implement service logic
        ...
