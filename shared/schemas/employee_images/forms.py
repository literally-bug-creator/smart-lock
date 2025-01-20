from dataclasses import dataclass, field

from fastapi import File, UploadFile

from shared.schemas.common import (BaseForm, PydanticUploadFile,
                                   convert_dc_to_pd)


class Create(BaseForm):
    file: PydanticUploadFile


@dataclass
class _CreateDC:
    file: UploadFile = File(...)


class Update(BaseForm):
    file: PydanticUploadFile
    vector: list


@dataclass
class _UpdateDC:
    file: UploadFile = File(...)
    vector: list = field(default_factory=list)


create = convert_dc_to_pd(_CreateDC, Create)
update = convert_dc_to_pd(_UpdateDC, Update)