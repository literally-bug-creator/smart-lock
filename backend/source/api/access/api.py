from fastapi import APIRouter, Depends, status
from services.access import AccessService
from schemas.access import params, forms

from .settings import PREFIX, Path

router = APIRouter(prefix=PREFIX, tags=["Access"])


@router.post(
    path=Path.WEBHOOK,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {},
        status.HTTP_401_UNAUTHORIZED: {}
    },
)
async def webhook(
    pms: params.Webhook = Depends(),
    form: forms.Webhook = Depends(forms.webhook),
    service: AccessService = Depends(),
) -> None:
    return await service.webhook(pms, form)
