from bs4 import BeautifulSoup as BS
from pytube import YouTube, Playlist, Search

s = Search('master of puppets')

print(s.results)