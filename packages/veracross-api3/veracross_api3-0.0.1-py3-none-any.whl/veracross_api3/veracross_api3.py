import requests
import time
import datetime
from urllib import parse


class Veracross:
    def __init__(self, config):
        self.bearer_token = None
        self.school = config["school"]
        self.token_url = f"https://accounts.veracross.com/{self.school}/oauth/token"
        self.api_base_url = f"https://api.veracross.com/{self.school}/v3/"
        self.client_id = config["client_id"]
        self.client_secret = config["client_secret"]
        self.scopes = config["scopes"]

        self.page_size = 1000

        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json',
                                     'X-Page-Size': str(self.page_size)
                                     })

        self.token_expire_time = datetime.datetime.now() - datetime.timedelta(days=1)

        self.rate_limit_remaining = 300
        self.rate_limit_reset = 0

    def __repr__(self):
        if self.bearer_token:
            return "Veracross_API3 connected to self.api_base_url"
        else:
            return "Veracross_API3"

    def get_authorization_token(self):
        """
        Get / refresh bearer token from veracross api.
        :return: string: bearer token
        """
        s = requests.Session()

        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            payload = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials',
                'scope': ' '.join(self.scopes)
            }
            r = s.post(self.token_url, data=payload, headers=headers)
            json = r.json()

            self.bearer_token = json["access_token"]
            self.session.headers.update({'Authorization': 'Bearer ' + self.bearer_token})

            return json["access_token"]
        except Exception as e:
            print(e)

    def check_rate_limit(self, headers):
        if "X-Rate-Limit-Remaining" in headers:
            self.rate_limit_remaining = int(headers["X-Rate-Limit-Remaining"])

            now = int(datetime.datetime.now().strftime("%s"))
            reset = int(headers["X-Rate-Limit-Reset"])
            wait = reset - now
            self.rate_limit_reset = int(wait)

            if int(headers["X-Rate-Limit-Remaining"]) < 2:
                print("VC rate limit reached. Waiting {} seconds.".format(wait))
                time.sleep(wait)
        else:
            return False

    def pull(self, endpoint, parameters=None):
        """
        Pull requested data from veracross api.
        :return: data
        """
        self.get_authorization_token()

        if parameters:
            url = self.api_base_url + endpoint + "?" + parse.urlencode(parameters, safe=':-')
        else:
            url = self.api_base_url + endpoint

        # Get first page
        page = 1
        r = self.session.get(url)

        if r.status_code == 401:
            # Possible a scope is missing
            print(r.text)
            return None

        if r.status_code == 200:
            self.check_rate_limit(headers=r.headers)
            data = r.json()
            data = data['data']
            last_count = len(data)
        else:
            return None

        # Any other pages to get?
        while last_count >= self.page_size:
            r = self.session.get(url,
                                 headers={'X-Page-Number': str(page + 1)})

            if r.status_code == 200:
                self.check_rate_limit(headers=r.headers)
                next_page = r.json()
                last_count = len(next_page['data'])
                data = data + next_page['data']

        return data
