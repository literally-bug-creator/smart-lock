from fastapi import Depends, HTTPException, status
from database.repos.employee_image import EmployeeImageRepo
from database.repos.employee import EmployeeRepo
from schemas.access import params, forms
from celery_service.tasks import get_face_vector


class AccessService:
    def __init__(
        self,
        repo: EmployeeImageRepo = Depends(),
        employee_repo: EmployeeRepo = Depends(),
    ):
        self.__repo = repo
        self.__employee_repo = employee_repo

    async def webhook(
        self, pms: params.Webhook, form: forms.Webhook
    ) -> None:
        image_bytes = await form.file.read()
        vector = get_face_vector.delay(image_bytes).get()
        if vector is None:
            raise HTTPException(status.HTTP_404_FORBIDDEN, "No face found!")
        employee_image = await self.__repo.get_nearest_by_vector(
            vector=vector,
        )
        if employee_image is None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "NO similar employee")  # noqa

        employee = await self.__employee_repo.get(id=employee_image.employee_id)
        if employee is None:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Database error")  # noqa

        if employee.access_level > pms.access_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied"
            )
