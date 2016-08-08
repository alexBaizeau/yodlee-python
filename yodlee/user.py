import requests
from jinja2 import Template
import webbrowser
import os
from urlparse import parse_qs
import urllib

HTML="""<div class='center processText'>Processing...</div>
<div>
<form action='{url}' method='post' id='rsessionPost'>
    RSession : <input type='text' name='rsession' placeholder='rsession' value='{rsession}' id='rsession'/><br/>
    FinappId : <input type='text' name='app' placeholder='App' value='{app}' id='finappId'/><br/>
    Redirect : <input type='text' name='redirectReq' placeholder='true/false' value='true'/><br/>
    Token : <input type='text' name='token' placeholder='token' value='{token}' id='token'/><br/>
    Extra Params : <input type='text' name='extraParams' placeholer='Extra Params' value='{extra_params}' id='extraParams'/><br/>
</form></div>
<script>document.getElementById('rsessionPost').submit();</script>"""


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

    def get_provider_accounts(self):

        url = "{}/v1/providers/providerAccounts".format(self.cobrand.host)
        response = requests.get(url, headers=self.build_auth_headers())
        return response.json()['providerAccount']

    def get_provider_account(self, account_id):

        url = "{}/v1/providers/providerAccounts/{}?include=credentials".format(self.cobrand.host, account_id)
        response = requests.get(url, headers=self.build_auth_headers())


    def get_fastlink_iframe_link(self, extra_params):

        token_url = "{}/v1/providers/token".format(self.cobrand.host)

        response = requests.get(token_url, headers=self.build_auth_headers()).json()
        params = parse_qs(response['parameters'])
        payload = {
            'app': params['app'][0],
            'redirectReq': params['redirectReq'][0],
            'token': params['token'][0],
            'rsession': params['rsession'][0],
            'url': response['url'],
            'extra_params': urllib.urlencode(extra_params)
        }

        html_content = HTML.format(**payload)
        fobj = open("post.html", "wb")
        fobj.write(html_content.encode('utf-8'))
        fobj.close()
        abs_file_path = os.path.abspath(fobj.name)
        webbrowser.open("file://"+abs_file_path)
        print payload
