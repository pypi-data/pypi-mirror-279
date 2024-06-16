from .Exceptions import TesAPIClientException, TesAPIConnectError, TesAPIUnknownError
from .Timer import Timer
from requests import post, get

class response:
    def __init__(self, content, response_code, interval: float):
        self.message = content
        self.code = response_code
        self.request_time = interval

class Client:
    def __init__(self, *, User: str = None, Token: str = None, end_point: str = "http://167.235.13.16:21689"):
        if User is None:
            raise TesAPIClientException("User is none")
        if Token is None:
            raise TesAPIClientException("Token is none")
        self.User, self.Token, self.endpoint = User, Token, end_point

    def SendMessage(self, *, model: str, message: str, temperature: float = 1) -> response:
        time = 0
        try:
            timer = Timer()
            timer.start()
            req = post(
                url=self.endpoint+"/ai/{}".format(model),
                json={
                    "message": message,
                    "parameters": {
                        "temperature": temperature
                    }
                },
                headers={
                    "User": self.User,
                    "Token": self.Token
                }
            ).json()
            timer.stop()
            time = timer.get_interval()
        except ConnectionError as e:
            raise TesAPIConnectError("Failed to connect to TesAPI")
        except Exception as e:
            raise TesAPIUnknownError("There was an unknown error encountered while attempting to connect to TesAPI.")

        return response(req["output"], req["response"]["ResponseCode"], time)

    def GetTokenCoins(self) -> float | str:
        req = post(
            url=self.endpoint+"/api/ai-coins/{}".format(self.User),
            headers = {
                "Token": self.Token
            }
        ).json()
        return req["output"]
    
    def GetModels(self) -> dict:
        try:
            req = get(
                url=self.endpoint+"/ai-models"
            ).json()
        except ConnectionError:
            raise TesAPIConnectError("Failed to connect to TesAPI")
        except Exception:
            raise TesAPIUnknownError("There was an unknown error encountered while attempting to connect to TesAPI")
        return req
