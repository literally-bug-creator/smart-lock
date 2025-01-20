from .base import BaseAPI, RequestData, ResponseData
from shared.schemas.employee_images import params, bodies, forms, responses

class EmployeeImagesAPI(BaseAPI):
    def __init__(self, url: str, timeout: float = 5.0):
        super().__init__(f"{url}/employees", timeout)

    async def update(
        self,
        params: params.Update,
        #body: bodies.Update,
        form: forms.Update,
    ) -> ResponseData[responses.Update]: # type: ignore
        data = RequestData(
            method_type="patch",
            path=f"/{params.employee_id}/images/{params.id}",
            #body=body,
            data=form.model_dump(exclude_none=True),
            response_type=responses.Update,
        )
        return await self._request(data)

    async def delete(
        self,
        params: params.Delete,
    ) -> ResponseData[None]:
        data = RequestData(
            method_type="delete",
            path=f"/{params.employee_id}/images/{params.id}",
            response_type=None,
        )
        return await self._request(data)
