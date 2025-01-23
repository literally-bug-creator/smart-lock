from dataclasses import dataclass, field

from fastapi import File, UploadFile, Form

from shared.schemas.common import BaseForm, PydanticUploadFile, convert_dc_to_pd


class Create(BaseForm):
    file: PydanticUploadFile


@dataclass
class _CreateDC:
    file: UploadFile = File(...)


class Update(BaseForm):
    file: PydanticUploadFile | None = None
    vector: list | None = None


@dataclass
class _UpdateDC:
    file: UploadFile | None = File(None)
    vector: list | None = Form(None)


create = convert_dc_to_pd(_CreateDC, Create)
update = convert_dc_to_pd(_UpdateDC, Update)
