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
date = datetime.now(jst)
token = 'AIzaSyAKMLTjQo6_MiQ5kSTH04M0BZvuYLcEZvU'
query = 'vocaloid'
query_url = f'https://www.googleapis.com/youtube/v3/search?key={token}&type=video&part=snippet&q={query}'

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

def main(p, q):
  res = requests.get(query_url).json()
  for i in range(5):
    if res['items'][i]['id']['videoId']:
      url = f'https://www.youtube.com/watch?v={res["items"][i]["id"]["videoId"]}'
      payload = {"text": f'{date.ctime()}\n{url}'}
      oauth.post("https://api.twitter.com/2/tweets", json=payload)

if __name__ == '__main__':
  main()
