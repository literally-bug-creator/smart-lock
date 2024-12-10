class EmployeeImagesService:
    def __init__(
            self,
            user: "User" = Depends(get_current_user),
    ):
        pass

    async def create(self) -> ...:  # TODO: Implement service logic
        ...

    async def read(self) -> ...:  # TODO: Implement service logic
        ...

    async def delete(self) -> ...:  # TODO: Implement service logic
        ...

    async def list(self) -> ...:  # TODO: Implement service logic
        ...

