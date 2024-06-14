from shuttleasgi.messages import Request

import uuid


class RequestIDMiddleware:
    def __init__(self, header_name: bytes = b"X-Request-ID") -> None:
        self.header_name = header_name
        self.prefix = b"req_"

    async def __call__(self, request: Request, handler):
        value = self.prefix + uuid.uuid4().hex.encode()

        response = await handler(request)

        request.add_header(self.header_name, value)

        return response
