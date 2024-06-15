from .Exceptions import TesAPIClientException
from requests import post


class response:
    def __init__(self, content, response_code):
        self.message = content
        self.code = response_code

class Client:
    def __init__(self, *, User: str = None, Token: str = None, end_point: str = "http://167.235.13.16:21689"):
        if User is None:
            raise TesAPIClientException("User is none")
        if Token is None:
            raise TesAPIClientException("Token is none")
        self.User, self.Token, self.endpoint = User, Token, end_point

    def SendMessage(self, *, model: str, message: str) -> response:
        req = post(
            url=self.endpoint+"/ai/{}".format(model),
            json={"message": message},
            headers={
                "User": self.User,
                "Token": self.Token
            }
        ).json()



        return response(req["output"], req["response"]["ResponseCode"])

    def GetTokenCoins(self) -> float | str:
        req = post(
            url=self.endpoint+"/api/ai-coins/{}".format(self.User),
            headers = {
                "Token": self.Token
            }
        ).json()
        return req["output"]
