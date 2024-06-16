class TesAPIClientException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TesAPIConnectError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class TesAPIUnknownError(Exception):
    def __init__(self, message: str):
        super().__init__(message)