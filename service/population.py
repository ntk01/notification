from requests_oauthlib import OAuth1Session
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import firebase_admin
from firebase_admin import firestore
import model.country as country

app = firebase_admin.initialize_app()
db = firestore.client()

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

jst = timezone(timedelta(hours=+9), 'JST')
date = datetime.now(jst)
today = date.strftime('%Y%m%d')
yesterday = (date - timedelta(days=1)).strftime('%Y%m%d')

japan = "japan"
us = "us"
china = "china"

ja_url = 'https://www.worldometers.info/world-population/japan-population/'
us_url = 'https://www.worldometers.info/world-population/us-population/'
ch_url = 'https://www.worldometers.info/world-population/china-population/'

def getTarget(url):
  req = requests.get(url)
  soup = BeautifulSoup(req.content, features='html.parser')
  return soup.find('div', attrs={'class': 'col-md-8 country-pop-description'}).find_all_next('strong')[1]

def replaceComma(target):
  if target:
    return int(target.replace(',', ''))
  else:
    return None

def getPopulation(name, date):
  doc_id = date + name
  doc = db.collection("countries").document(doc_id).get()
  return doc.to_dict().get('population')

def setPopulation(name, date, population):
  doc_id = date + name
  db.collection("countries").document(doc_id).set(vars(country.Country(name=name, population=population)))

def formatPopulation(number):
  n = "{:,}".format(number)
  if 0 < number:
    n = "+" + n
  return n

ja_target = getTarget(ja_url).text
us_target = getTarget(us_url).text
ch_target = getTarget(ch_url).text

ja_cnt = replaceComma(ja_target)
us_cnt = replaceComma(us_target)
ch_cnt = replaceComma(ch_target)

prev_ja_cnt = getPopulation("japan", yesterday)
prev_us_cnt = getPopulation("us", yesterday)
prev_ch_cnt = getPopulation("china", yesterday)

diff_ja = "undefined" if prev_ja_cnt == None else formatPopulation(ja_cnt - prev_ja_cnt)
diff_us = "undefined" if prev_us_cnt == None else formatPopulation(us_cnt - prev_us_cnt)
diff_ch = "undefined" if prev_ch_cnt == None else formatPopulation(ch_cnt - prev_ch_cnt)

text = f'【定時取得】\n日時: {date.ctime()}\n\n日本: {ja_target} (前日比 {diff_ja})\nアメリカ: {us_target} (前日比 {diff_us})\n中国: {ch_target} (前日比 {diff_ch})\n\n取得元: https://www.worldometers.info/'
payload = {"text": text}

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

def postTweet(p, q):
  setPopulation(japan, today, ja_cnt)
  setPopulation(us, today, us_cnt)
  setPopulation(china, today, ch_cnt)
  oauth.post("https://api.twitter.com/2/tweets", json=payload)
