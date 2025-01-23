from pydantic import BaseModel


class Update(BaseModel):
    image_vector: list
    file_key: str
