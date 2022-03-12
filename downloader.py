import requests
from bs4 import BeautifulSoup as BS
from pytube import Search
import tkinter as tk
from pydub import AudioSegment
import os


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
        print(f'Baixando {s.results[0].title}')
        stream = s.results[0].streams.get_by_itag(251)
        stream.download(output_path=f"{os.path.abspath(os.path.join(os.path.abspath(os.path.join('downloader.py', os.pardir)), os.pardir))}/{soup.find(class_='iJkkJW').string}")
        print(f'Convertendo {stream.default_filename} para MP3')
        AudioSegment.from_file(f"{os.path.abspath(os.path.join(os.path.abspath(os.path.join('downloader.py', os.pardir)), os.pardir))}/{soup.find(class_='iJkkJW').string}/{stream.default_filename}").export(f"{os.path.abspath(os.path.join(os.path.abspath(os.path.join('downloader.py', os.pardir)), os.pardir))}/{soup.find(class_='iJkkJW').string}/{stream.default_filename}.mp3", format="mp3")
        os.remove(f"{os.path.abspath(os.path.join(os.path.abspath(os.path.join('downloader.py', os.pardir)), os.pardir))}/{soup.find(class_='iJkkJW').string}/{stream.default_filename}")
        print(f'{s.results[0].title} - Salvo com sucesso')
    root.destroy()

button = tk.Button(root, text="Baixar", command=downloader)
button.pack()
root.mainloop()