from yodlee.cobrand import Cobrand
from yodlee.user import User
import ConfigParser


Config = ConfigParser.ConfigParser()
Config.read("config.ini")

cobrand_login = Config.get('cobrand', 'login')
cobrand_password = Config.get('cobrand', 'password')

user_login = Config.get('user', 'login')
user_password = Config.get('user', 'password')

url = Config.get('cobrand', 'host')

if __name__ == '__main__':

    cobrand = Cobrand(url, cobrand_login, cobrand_password)
    user = User(cobrand, user_login, user_password)

    accounts = user.get_accounts()
    for account in accounts['account']:
        print account['id']
        print account['accountName']

    provider_accounts = user.get_provider_accounts()
    print provider_accounts
    account_to_refresh = provider_accounts[0]['id']
    account_to_edit = provider_accounts[1]['id']

    user.get_provider_account(account_to_refresh)

    # When a user exits out of Fastlink they get redirected here.
    callback_url = 'http://requestb.in/1c12mkr1'

    refresh_account_extra_params = {
        'siteAccountId':  account_to_refresh,
        'flow': 'refresh',
        'callback': callback_url
    }

    add_account_extra_params = {
        'callback': callback_url
    }

    edit_account_extra_params = {
        'siteAccountId':  account_to_refresh,
        'flow': 'edit',
        'callback': callback_url
    }

    user.get_fastlink_iframe_link(add_account_extra_params)
    user.get_fastlink_iframe_link(refresh_account_extra_params)
    user.get_fastlink_iframe_link(edit_account_extra_params)
