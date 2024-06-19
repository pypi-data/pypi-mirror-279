import http.client
import io

from hrfh.models import HTTPResponse


class FakeSocket:
    def __init__(self, bytes_stream):
        self._file = bytes_stream

    def makefile(self, *args, **kwargs):
        return self._file


def load_from_byte_stream(data: bytes) -> HTTPResponse:
    response_stream = FakeSocket(io.BytesIO(data))
    response = http.client.HTTPResponse(response_stream)
    response.begin()
    return HTTPResponse(
        ip="1.1.1.1",
        port=80,
        version=response.version,
        status_code=response.status,
        status_reason=response.reason,
        # NOTE: the order of headers will be lost if we insist to use response.getheaders()
        headers=response.getheaders(),
        body=response.read(),
    )
