from requests_oauthlib import OAuth1Session
import os
from googleapiclient.discovery import build
import service.random as r

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

def main(p, q):
  text = r.getText()
  payload = {"text": text}
  print(payload)
  # res = oauth.post("https://api.twitter.com/2/tweets", json=payload)
  r.setOne()
  # print(res)

if __name__ == '__main__':
  main()
