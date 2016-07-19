import requests


class Cobrand(object):

    def __init__(self, host, login, password):
        self.login = login
        self.password = password
        self.host = host

        login_url = "{}/v1/cobrand/login".format(self.host)

        payload = {
            "cobrand": {
                "cobrandLogin": self.login,
                "cobrandPassword": self.password,
                "locale": "en_US"
            }
        }

        response = requests.post(login_url, json=payload).json()
        self.session_token = response['session']['cobSession']

    def build_auth_headers(self):
        headers = {
            "Authorization": "{{cobSession={0}}}".format(self.session_token)
        }
        return headers
