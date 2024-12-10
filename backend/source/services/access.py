from api.users import current_active_user
from fastapi import Depends, HTTPException, status


class AccessService:
    def __init__(
        self,
        user: "User" = Depends(get_current_user),
    ):
        pass

    async def read(self) -> None:  # TODO: Implement service logic
        ...