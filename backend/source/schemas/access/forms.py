from dataclasses import dataclass
from fastapi import File, UploadFile
from shared.schemas.common import (BaseForm, PydanticUploadFile,
                                   convert_dc_to_pd)


class Webhook(BaseForm):
    file: PydanticUploadFile


@dataclass
class _WebhookDC:
    file: UploadFile = File(...)


webhook = convert_dc_to_pd(_WebhookDC, Webhook)