class TTSClient:
    def __init__(self, server_url: str, timeout: int = 300) -> None:
        self.server_url = server_url.rstrip("/")
        self.timeout = timeout
