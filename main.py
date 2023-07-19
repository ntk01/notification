from requests_oauthlib import OAuth1Session
import os
from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

jst = timezone(timedelta(hours=+9), 'JST')
date = datetime.now(jst)
token = 'AIzaSyAKMLTjQo6_MiQ5kSTH04M0BZvuYLcEZvU'
query = 'vocaloid'
youtube = build('youtube', 'v3', developerKey=token)

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

def main(p, q):
  res = youtube.search().list(
    part='snippet',
    q=query,
    maxResults=5,
    order='rating',
    type='video',
  ).execute()
  for i in range(5):
    if res['items'][i]['id']['videoId']:
      url = f'https://www.youtube.com/watch?v={res["items"][i]["id"]["videoId"]}'
      payload = {"text": f'{date.ctime()}\n{url}'}
      oauth.post("https://api.twitter.com/2/tweets", json=payload)

if __name__ == '__main__':
  main()
