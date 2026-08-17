import httpx


class HTTPClient:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    async def get(self, url: str, **kwargs):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, **kwargs)
            response.raise_for_status()
            return response

    async def post(self, url: str, **kwargs):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, **kwargs)
            response.raise_for_status()
            return response