import requests
from bs4 import BeautifulSoup as BS
from pytube import Search
import tkinter as tk
from tkinter import ttk
from pydub import AudioSegment
import os


root = tk.Tk()
root.title('Downloader')

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text='Digite o link da playlist:').grid(column=0, row=0)
entry = ttk.Entry(mainframe)
entry.grid(column=0, row=1)

log = tk.Text(mainframe, width=80, height=24, wrap='none')
log.grid(column=0, row=3)

def writeToLog(msg):
    numlines = int(log.index('end - 1 line').split('.')[0])
    log['state'] = 'normal'
    if numlines==24:
        log.delete(1.0, 2.0)
    if log.index('end-1c')!='1.0':
        log.insert('end', '\n')
    log.insert('end', msg)
    log['state'] = 'disabled'

def downloader():
    source = entry.get()
    site = requests.get(source).content
    soup = BS(site, 'html.parser')
    lista = soup.find_all(class_="eWYxOj")
    for i in lista:
        root.update()
        s = Search(f"Music {i.string} {i.find_next('a').string}")
        writeToLog(f'Baixando {s.results[0].title}')
        root.update()
        stream = s.results[0].streams.get_by_itag(251)
        stream.download(output_path=f"{os.path.abspath(os.path.join(os.path.abspath(os.path.join('downloader.py', os.pardir)), os.pardir))}/{soup.find(class_='iJkkJW').string}")
        writeToLog(f'Convertendo {stream.default_filename} para MP3')
        root.update()
        AudioSegment.from_file(f"{os.path.abspath(os.path.join(os.path.abspath(os.path.join('downloader.py', os.pardir)), os.pardir))}/{soup.find(class_='iJkkJW').string}/{stream.default_filename}").export(f"{os.path.abspath(os.path.join(os.path.abspath(os.path.join('downloader.py', os.pardir)), os.pardir))}/{soup.find(class_='iJkkJW').string}/{stream.default_filename}.mp3", format="mp3")
        os.remove(f"{os.path.abspath(os.path.join(os.path.abspath(os.path.join('downloader.py', os.pardir)), os.pardir))}/{soup.find(class_='iJkkJW').string}/{stream.default_filename}")
        writeToLog(f'{s.results[0].title} - Salvo com sucesso')
        root.update()
    writeToLog('Playlist baixada com sucesso!')

ttk.Button(mainframe, text="Baixar", command=downloader).grid(column=0, row=2)

root.mainloop()