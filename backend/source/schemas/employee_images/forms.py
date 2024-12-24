from dataclasses import dataclass

from fastapi import File, UploadFile

from schemas.common import (BaseForm, PydanticUploadFile,
                                   convert_dc_to_pd)


class Create(BaseForm):
    file: PydanticUploadFile


@dataclass
class _CreateDC:
    file: UploadFile = File(...)


create = convert_dc_to_pd(_CreateDC, Create)