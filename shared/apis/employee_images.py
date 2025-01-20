from .base import BaseAPI, RequestData, ResponseData
from shared.schemas.employee_images import params, bodies, responses


class EmployeeImagesAPI(BaseAPI):
    def __init__(self, url: str, timeout: float = 5.0):
        super().__init__(f"{url}/employees", timeout)

    async def update(
        self,
        params: params.Update,
        body: bodies.Update,
    ) -> ResponseData[responses.Update]:  # type: ignore
        data = RequestData(
            method_type="patch",
            path=f"/{params.employee_id}/images/{params.id}",
            body=body,
            response_type=responses.Update,
        )
        return await self._request(data)

    async def delete(
        self,
        params: params.Delete,
    ):
        data = RequestData(
            method_type="delete",
            path=f"/{params.employee_id}/images/{params.id}",
        )
        return await self._request(data)
