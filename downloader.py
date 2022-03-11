import requests
from bs4 import BeautifulSoup as BS
from pytube import YouTube, Playlist, Search

source = ('https://open.spotify.com/playlist/1z6axQOw8P27J7ysXtflql')

site = requests.get(source).content

soup = BS(site, 'html.parser')

lista = soup.find_all(class_="eWYxOj")

for i in lista:
    s = Search(f"Music {i.string} {i.find_next('a').string}")

    stream = s.results[0].streams.get_by_itag(251)
    stream.download()