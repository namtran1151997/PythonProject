import requests
from bs4 import BeautifulSoup
import re
import json
import pprint as pp

r = requests.get('https://www.instagram.com/explore/tags/ny/')
soup = BeautifulSoup(r.content, 'lxml')
scripts = soup.find_all('script', type="text/javascript", text=re.compile('window._sharedData'))

stringified_json = scripts[0].get_text().replace('window._sharedData = ', '')[:-1]

# print(json.loads(stringified_json)['entry_data']['ProfilePage'][0])
pp.pprint(json.loads(stringified_json)['entry_data'])