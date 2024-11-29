import requests
from .settings import ServerAPISettings
from .exceptions import RequestIdentifyError


class ServerAPI:
    def __init__(self, settings: ServerAPISettings) -> None:
        self.__settings = settings

    def request_identify(self, frame_path) -> bool:
        if self.__settings.URL is None:
            return False

        try:
            return self._request_identify(frame_path)

        except requests.exceptions.RequestException as e:
            raise RequestIdentifyError(f"Network or HTTP error while identifying request: {str(e)}") from e
        except ValueError as e:
            raise RequestIdentifyError(f"Invalid value error: {str(e)}") from e
        except FileNotFoundError as e:
            raise RequestIdentifyError(f"File not found: {frame_path}. Error: {str(e)}") from e

    def _request_identify(self, frame_path):
        with open(frame_path, "rb") as frame:
            request = requests.post(
                self.__settings.URL, files={"file": ("frame.png", frame, "image/png")}
            )

            return request.status_code == 200


def get_server_api():
    settings = ServerAPISettings()  # type: ignore
    server_api = ServerAPI(settings)
    return server_api
