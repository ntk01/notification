import os
import requests

token = 'AIzaSyAKMLTjQo6_MiQ5kSTH04M0BZvuYLcEZvU'
query = 'vocaloid'
url = f'https://www.googleapis.com/youtube/v3/search?key={token}&type=video&part=snippet&q={query}'

def main(p, q):
  res = requests.get(url).json()
  print(res)

if __name__ == '__main__':
  main()
