from typing import TYPE_CHECKING

from api.users import current_active_user
from fastapi import Depends

if TYPE_CHECKING:
    from database.models import User


class EmployeeService:
    def __init__(
        self,
        user: "User" = Depends(current_active_user),
    ):
        pass

    async def create(self) -> ...:  # TODO: Implement service logic
        ...

    async def read(self) -> ...:  # TODO: Implement service logic
        ...

    async def update(self) -> ...:  # TODO: Implement service logic
        ...

    async def delete(self) -> ...:  # TODO: Implement service logic
        ...

    async def list(self) -> ...:  # TODO: Implement service logic
        ...
