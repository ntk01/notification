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

ja_req = requests.get('https://www.worldometers.info/world-population/japan-population/')
us_req = requests.get('https://www.worldometers.info/world-population/us-population/')
ch_req = requests.get('https://www.worldometers.info/world-population/china-population/')
ja_soup = BeautifulSoup(ja_req.content, features='html.parser')
us_soup = BeautifulSoup(us_req.content, features='html.parser')
ch_soup = BeautifulSoup(ch_req.content, features='html.parser')

ja_target = ja_soup.find('div', attrs={'class': 'col-md-8 country-pop-description'}).find_all_next('strong')[1]
us_target = us_soup.find('div', attrs={'class': 'col-md-8 country-pop-description'}).find_all_next('strong')[1]
ch_target = ch_soup.find('div', attrs={'class': 'col-md-8 country-pop-description'}).find_all_next('strong')[1]

text = f'【人口取得】\n日時: {datetime.now(jst).ctime()}\n\n日本: {ja_target.text}\nアメリカ: {us_target.text}\n中国: {ch_target.text}\n\n取得元: https://www.worldometers.info/'

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
