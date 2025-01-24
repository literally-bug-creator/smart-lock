import requests
from .settings import ServerAPISettings


class ServerAPI:
    def __init__(self, settings: ServerAPISettings) -> None:
        self.__settings = settings

    def request_identify(self, frame_bytes) -> bool:
        if self.__settings.URL is None:
            return False
        
        return self._request_identify(frame_bytes)

    def _request_identify(self, frame_bytes):
        request = requests.post(
            url=self.__settings.URL,
            params={"access_level": self.__settings.ACCESS_LEVEL},
            files={"file": ("frame.png", frame_bytes, "image/png")},
            verify=False,
        )

        return request.status_code == 200


def get_server_api():
    settings = ServerAPISettings()  # type: ignore
    server_api = ServerAPI(settings)
    return server_api
