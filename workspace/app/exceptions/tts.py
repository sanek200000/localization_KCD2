class TTSClientError(Exception):
    pass


class TTSConnectionError(TTSClientError):
    pass


class TTSServerError(TTSClientError):
    pass
