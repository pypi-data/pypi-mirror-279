from typing import List, Tuple

from bs4 import BeautifulSoup

from hrfh.utils.hash import sha256sum
from hrfh.utils.mask import mask_sentence
from hrfh.utils.tokenize import tokenize_html


class HTTPResponse:
    def __init__(
        self,
        ip: str = "",
        port: int = 80,
        version: str = "HTTP/1.1",
        status_code: int = 200,
        status_reason: str = "OK",
        headers: List[Tuple[str, str]] = [],
        body: bytes = b"",
    ):
        self.ip = ip
        self.port = port
        self.version = version
        if self.version == 10:
            self.version = "HTTP/1.0"
        if self.version == 11:
            self.version = "HTTP/1.1"
        self.status_code = status_code
        self.status_reason = status_reason
        self.headers = headers
        self.body = body
        self.masked: str = self._mask()

    def __repr__(self) -> str:
        return f"<HTTPResponse {self.ip}:{self.port} {self.status_code} {self.status_reason}>"

    def _mask(self) -> str:
        return self._preprocess()

    def fuzzy_hash(self, hasher=sha256sum) -> str:
        return hasher(self.masked)

    def _preprocess(self) -> str:
        soup = BeautifulSoup(self.body, "html.parser")
        tokens = tokenize_html(soup)
        masked_html_tokens = []
        for token in tokens:
            if token.startswith("<") and token.endswith(">"):
                # append html tags
                masked_html_tokens.append(token)
            else:
                # append masked text content
                # TODO: handle random string in javascript by create a abstract syntax tree [1] for <script> tag
                # [1] https://github.com/tree-sitter/py-tree-sitter
                masked_html_tokens.append(mask_sentence(token))
        header_lines = []
        strip_headers = [
            "Expires",
            "Date",
            "Content-Length",
            "Location",
            "Via",
            "via",
            "Last-Modified",
        ]
        shoud_not_mask_headers = [
            "Server",
            "Connection",
            "Content-Type",
            "Content-Encoding",
            "Cache-Control",
        ]
        headers = []
        if type(self.headers) is dict:
            headers = self.headers.items()
        else:
            headers = self.headers
        for key, value in headers:
            if key in strip_headers:
                value = ""
            elif key in shoud_not_mask_headers:
                value = value
            else:
                value = mask_sentence(value)
            header_lines.append(f"{key}: {value}")
        lines = [f"{self.version} {self.status_code} {self.status_reason}"]
        lines += sorted(header_lines)
        lines += masked_html_tokens
        return "\n".join(lines)
