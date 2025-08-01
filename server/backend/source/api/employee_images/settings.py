from enum import StrEnum

PREFIX = "/employees/{employee_id}/images"


class Path(StrEnum):
    CREATE = ""
    READ = "/{id}"
    UPDATE = "/{id}"
    DELETE = "/{id}"
    DELETE_ALL = ""
    LIST = ""
