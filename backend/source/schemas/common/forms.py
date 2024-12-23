from fastapi import Depends, UploadFile
from pydantic import BaseModel, PlainSerializer
from typing import Callable, Annotated, Any


def convert_dc_to_pd[DC, PD: BaseModel](dc_t: type[DC], pd_t: type[PD]) -> Callable[[DC], PD]:
    def wrapper(data=Depends(dc_t)) -> PD:
        return pd_t.model_validate(data, from_attributes=True)
    return wrapper


class FormField:
    value: Any
    filename: str | None = None
    content_type: str | None = None
    content_transfer_encoding: str | None = None

    def __init__(
        self,
        value: Any,
        filename: str | None = None,
        content_type: str | None = None,
        content_transfer_encoding: str | None = None,
    ):
        self.value = value
        self.filename = filename
        self.content_type = content_type
        self.content_transfer_encoding = content_transfer_encoding

    def dict(self) -> dict[str, Any]:
        return {
            "value": self.value,
            "filename": self.filename,
            "content_type": self.content_type,
            "content_transfer_encoding": self.content_transfer_encoding,
        }


def __serialize_upload_file(value: UploadFile) -> FormField:
    return FormField(
        value=value.file.read(),
        filename=value.filename,
        content_type=value.content_type,
    )


PydanticUploadFile = Annotated[UploadFile, PlainSerializer(__serialize_upload_file)]  # noqa


class BaseForm(BaseModel):
    class Config:
        arbitrary_types_allowed = True
