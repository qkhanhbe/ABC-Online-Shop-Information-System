"""Presentation layer: minimal HTTP plumbing on top of WSGI (standard library only).

Request parses the query string, url-encoded forms and multipart uploads (search by image);
Response carries the HTML produced by a view. Sessions are kept in memory and identified by
a random cookie - enough for a prototype, replaced by a server-side store in production.
"""
import secrets
from email.parser import BytesParser
from email.policy import default as default_policy
from http.cookies import SimpleCookie
from urllib.parse import parse_qs

SESSIONS = {}
STATUS_TEXT = {200: "200 OK", 302: "302 Found", 400: "400 Bad Request", 403: "403 Forbidden",
               404: "404 Not Found", 500: "500 Internal Server Error"}


class Request:

    def __init__(self, environ):
        self.method = environ.get("REQUEST_METHOD", "GET").upper()
        self.path = environ.get("PATH_INFO", "/") or "/"
        self.query = {k: v[0] for k, v in parse_qs(environ.get("QUERY_STRING", "")).items()}
        self.form, self.files = {}, {}
        cookie = SimpleCookie(environ.get("HTTP_COOKIE", ""))
        self.session_id = cookie["sid"].value if "sid" in cookie else None
        if self.method == "POST":
            self._read_body(environ)

    def _read_body(self, environ):
        length = int(environ.get("CONTENT_LENGTH") or 0)
        body = environ["wsgi.input"].read(length) if length else b""
        ctype = environ.get("CONTENT_TYPE", "")
        if ctype.startswith("multipart/form-data"):
            message = BytesParser(policy=default_policy).parsebytes(
                b"Content-Type: " + ctype.encode() + b"\r\n\r\n" + body)
            for part in message.iter_parts():
                name = part.get_param("name", header="content-disposition")
                filename = part.get_filename()
                if filename:
                    content = part.get_payload(decode=True) or b""
                    if content:
                        self.files[name] = (filename, content)
                elif name:
                    self.form[name] = part.get_content().strip()
        else:
            self.form = {k: v[0] for k, v in parse_qs(body.decode("utf-8")).items()}

    def get(self, name, default=""):
        return self.form.get(name, self.query.get(name, default))

    @property
    def session(self):
        if self.session_id not in SESSIONS:
            self.session_id = secrets.token_hex(16)
            SESSIONS[self.session_id] = {}
        return SESSIONS[self.session_id]


class Response:

    def __init__(self, body="", status=200, content_type="text/html; charset=utf-8", headers=None):
        self.body = body if isinstance(body, bytes) else body.encode("utf-8")
        self.status = status
        self.headers = [("Content-Type", content_type)] + list(headers or [])

    @classmethod
    def redirect(cls, location, flash=None, request=None):
        if flash and request is not None:
            request.session["flash"] = flash
        return cls("", 302, headers=[("Location", location)])
