import requests
from pprint import pprint

r = requests.get('https://www.benzinga.com/api/news?channels=2&displayOutput=abstract&last=36043961&limit=20&offset=77&type=benzinga_reach%2Cstory')
pprint(r.json())