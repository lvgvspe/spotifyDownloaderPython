import requests
from bs4 import BeautifulSoup as BS
from pytube import Search
import tkinter as tk
from pydub import AudioSegment


root = tk.Tk()
label = tk.Label(text='Digite o link da playlist:')
label.pack()
entry = tk.Entry(root)
entry.pack()

def downloader():
    source = entry.get()
    site = requests.get(source).content
    soup = BS(site, 'html.parser')
    lista = soup.find_all(class_="eWYxOj")
    for i in lista:
        s = Search(f"Music {i.string} {i.find_next('a').string}")
        print(f'Downloading {s.results[0].title}')
        stream = s.results[0].streams.get_by_itag(251)
        stream.download(output_path=soup.find(class_='iJkkJW').string)
        AudioSegment.from_file(f"{soup.find(class_='iJkkJW').string}/{s.results[0].title}").export(f"{soup.find(class_='iJkkJW').string}/{s.results[0].title}", format="mp3")
    root.destroy()

button = tk.Button(root, text="Baixar", command=downloader)
button.pack()
root.mainloop()
