from usercheck.AbstractService import AbstractService
import requests


class Twitter(AbstractService):
    def __init__(self):
        super().__init__()
        self.name = 'twitter'

    def run(self, username):
        r = requests.get("https://twitter.com/" + username, headers={'User-Agent' : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/49.0"})

        return r.status_code != 200
