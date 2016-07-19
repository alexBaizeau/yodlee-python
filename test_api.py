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
