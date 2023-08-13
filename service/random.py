import requests
from datetime import datetime, timezone, timedelta
import firebase_admin
from firebase_admin import firestore
import random
import model.number as number

app = firebase_admin.initialize_app()
db = firestore.client()

jst = timezone(timedelta(hours=+9), 'JST')
date = datetime.now(jst)

n = random.choice(rand() + getAll())

def rand():
  return [*range(1, 101, 1)]

def getAll() -> list:
  docs = db.collection("numbers").stream()
  return list(map(lambda doc: doc.to_dict().get('number'), docs))

n = random.choice(rand() + getAll())

def setOne():
  db.collection("numbers").add(vars(number.Number(number=n)))

def getText():
  print(getAll())
  return f'{date.ctime()}\n\n1から100までの乱数を表示。\n表示した数字はDBにセット。\n1から100までの数列にDBから取得したリストを結合して乱数を表示。\n回を重ねると偏りが見られるかの実験。\n\n今選択されたのは...{n}'
