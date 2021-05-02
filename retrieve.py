import requests
from bs4 import BeautifulSoup as Soup


class Retrieve:
    def __init__(self, url):
        self.url = url

        req = requests.get(self.url)
        req_content = req.content.decode()
        soup = Soup(req_content, 'lxml')

        self.div = soup.find_all('div', {'class': "article-content"})[0]
        self.level = soup.find('span', {'class': "monster-level"}).text

    def mod_ac_and_saves(self):
        print(self.div)


retrieve = Retrieve("https://pf2.d20pfsrd.com/monster/black-dragon/")
retrieve.mod_ac_and_saves()
