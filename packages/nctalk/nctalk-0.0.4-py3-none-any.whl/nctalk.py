import hmac
import hashlib
from random import choice
from string import ascii_lowercase, ascii_uppercase, digits
import requests


class TalkMessenger:
    def __init__(self, endpoint_url: str, token: str, secret: str) -> None:
        self.secret = secret
        self.token = token
        self.random_str = self.random_string(32)
        self.endpoint_url = endpoint_url

    @staticmethod
    def random_string(size: int) -> str:
        allowed_values = ascii_lowercase + ascii_uppercase + digits
        return "".join(choice(allowed_values) for _ in range(size))

    @property
    def chat_url(self) -> str:
        return f"{self.endpoint_url}/ocs/v2.php/apps/spreed/api/v1/bot/{self.token}/message"

    def sign(self, message: str) -> str:
        hmac_sign = hmac.new(
            key=self.secret.encode("UTF-8"),
            msg=self.random_str.encode("UTF-8"),
            digestmod=hashlib.sha256,
        )
        hmac_sign.update(message.encode("UTF-8"))
        return hmac_sign.hexdigest()

    def send(self, message: str) -> bool:
        response = requests.post(
            self.chat_url,
            headers={
                "X-Nextcloud-Talk-Bot-Random": self.random_str,
                "X-Nextcloud-Talk-Bot-Signature": self.sign(message),
                "OCS-APIRequest": "true",
            },
            json={
                "message": message,
            },
        )
        return response.ok


def main_cli():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", required=True, help="Conversation channel ID")
    parser.add_argument("-s", "--secret", required=True, help="Shared secret key")
    parser.add_argument("-e", "--endpoint", required=True, help="NextCloud endpoint")
    parser.add_argument("-m", "--message", required=True, help="Message to sent")
    args = parser.parse_args()

    print("Args", args)

    messenger = TalkMessenger(
        endpoint_url=args.endpoint, token=args.token, secret=args.secret
    )
    messenger.send(args.message)


if __name__ == "__main__":
    main_cli()
