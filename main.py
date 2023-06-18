from requests_oauthlib import OAuth1Session
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

jst = timezone(timedelta(hours=+9), 'JST')

ja_url = 'https://www.worldometers.info/world-population/japan-population/'
us_url = 'https://www.worldometers.info/world-population/us-population/'
ch_url = 'https://www.worldometers.info/world-population/china-population/'

def getTarget(url):
  req = requests.get(url)
  soup = BeautifulSoup(req.content, features='html.parser')
  return soup.find('div', attrs={'class': 'col-md-8 country-pop-description'}).find_all_next('strong')[1]

ja_target = getTarget(ja_url)
us_target = getTarget(us_url)
ch_target = getTarget(ch_url)

text = f'【人口情報】\n日時: {datetime.now(jst).ctime()}\n\n日本: {ja_target.text}\nアメリカ: {us_target.text}\n中国: {ch_target.text}\n\n取得元: https://www.worldometers.info/'

payload = {"text": text}

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

def main(p, q):
  res = oauth.post("https://api.twitter.com/2/tweets", json=payload)
  print(res)

if __name__ == '__main__':
  main()
