import logging
from aiohttp import (
    ClientSession,
    ClientConnectionError,
    ClientError,
    ContentTypeError,
    ClientResponse,
    FormData,
)
from pydantic import BaseModel
from typing import Any
from fastapi import HTTPException, status
from shared.schemas.common import FormField


class RequestData[ResponseT](BaseModel):
    method_type: str
    path: str
    response_type: type[ResponseT] | None = None
    body: BaseModel | None = None
    query_params: dict[str, Any] | None = None
    data: dict[str, Any] | None = None
    headers: dict[str, str] | None = None


class ResponseData[ResponseT](BaseModel):
    class Config:
        arbitrary_types_allowed = True

    status_code: int
    data: ResponseT | None = None
    exception: Exception | None = None


class BaseAPI:
    def __init__(self, url: str, timeout: float = 5.0):
        self.url = url
        self.timeout = timeout

    def _init_client(self) -> ClientSession:
        return ClientSession()

    async def _request[ResponseT](self, request_data: RequestData[ResponseT]) -> ResponseData[ResponseT]:
        async with self._init_client() as session:
            return await self._send_request(session, request_data)

    async def _send_request[ResponseT](self, session: ClientSession, data: RequestData[ResponseT]) -> ResponseData[ResponseT]:
        method = getattr(session, data.method_type)
        payload = (
            data.body.model_dump(mode="json", exclude_none=True) if data.body else None
        )
        url = self.url + data.path
        params = self._flatten_params(data.query_params)
        form_data = self._extract_data(data.data)
        try:
            logging.error(f"Finally! {url=}")
            async with method(url, json=payload, data=form_data, params=params, timeout=self.timeout, headers=data.headers) as response:
                return await self._process_response(response, data.response_type)
        except (ClientConnectionError, TimeoutError):
            return ResponseData[ResponseT](
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                exception=HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Service unavailable"),  # noqa
            )
        except ClientError as e:
            logging.error("Client error", exc_info=e, stack_info=True)
            return ResponseData[ResponseT](
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                exception=HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Something went wrong"),  # noqa
            )

    def _flatten_params(self, params: dict[str, Any] | None) -> dict[str, str | int | float] | None:
        if params is None:
            return None
        result = dict()
        for key, value in params.items():
            if isinstance(value, dict):
                sub_params = self._flatten_params(value)
                if sub_params:
                    result |= sub_params
            elif isinstance(value, bool):
                result[key] = str(value).lower()
            else:
                result[key] = value
        return result

    def _extract_data(self, data: dict[str, Any] | None) -> FormData | None:
        if data is None:
            return None
        form = FormData()
        for key, value in data.items():
            if isinstance(value, FormField):
                form.add_field(key, **value.dict())
            elif isinstance(value, int | bool):
                form.add_field(key, str(value))
            else:
                form.add_field(key, value)
        return form

    async def _process_response[ResponseT](self, response: ClientResponse, response_model: type[ResponseT] | None) -> ResponseData[ResponseT]:
        json_data = await self._extract_json(response)
        if not 200 <= response.status < 300:
            return ResponseData[ResponseT](
                status_code=response.status,
                exception=HTTPException(response.status, **json_data),
            )
        data = response_model(**json_data) if response_model else None
        return ResponseData[ResponseT](
            status_code=response.status,
            data=data,
        )

    async def _extract_json(self, response: ClientResponse) -> dict[str, Any]:
        try:
            return await response.json()
        except ContentTypeError:
            return dict()


__all__ = [
    "BaseAPI",
    "RequestData",
    "ResponseData",
]
