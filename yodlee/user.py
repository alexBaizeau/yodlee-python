import requests


class User(object):

    def __init__(self, cobrand, login, password):
        self.cobrand = cobrand
        headers = cobrand.build_auth_headers()

        login_url = "{}/v1/user/login".format(cobrand.host)
        payload = {
            "user": {
                "loginName": login,
                "password": password,
                "locale": "en_US"
            }
        }

        response = requests.post(login_url,
                                 headers=headers, json=payload).json()

        self.user_session = response['user']['session']['userSession']

    def build_auth_headers(self):
        return {
            "Authorization": "{{cobSession={0}}},{{userSession={1}}}".format(
                self.cobrand.session_token, self.user_session)
        }

    def get_accounts(self):
        url = "{}/v1/accounts".format(self.cobrand.host)
        response = requests.get(url, headers=self.build_auth_headers())
        return response.json()
