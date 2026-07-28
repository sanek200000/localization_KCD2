import requests


class TTSClientError(Exception):
    pass


class TTSConnectionError(requests.ConnectionError):
    pass


class TTSServerError(TTSClientError):
    pass
