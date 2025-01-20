from .base import BaseRepo
from shared.database.models import EmployeeImage
from sqlalchemy import select
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shared.database import get_session
import os


class EmployeeImageRepo(BaseRepo[EmployeeImage]):
    MODEL = EmployeeImage

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session)
        self.__max_cos_dist = float(os.getenv("MAX_COSINE_DISTANCE", 0.06))

    async def get_nearest_by_vector(self, vector: list) -> EmployeeImage | None:
        return await self.session.scalar(
            select(EmployeeImage).filter(
                EmployeeImage.image_vector.cosine_distance(vector) < self.__max_cos_dist
            ))
