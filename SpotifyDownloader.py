import requests
from bs4 import BeautifulSoup as BS
from pytube import Search
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pydub import AudioSegment
import os
from distutils.dir_util import copy_tree
import threading
from pytube.exceptions import AgeRestrictedError

if not os.path.exists("C:/ffmpeg/bin"):
    copy_tree("ffmpeg", "C:/ffmpeg")
    os.system('cmd /c setx /m PATH "C:\\ffmpeg\\bin;%PATH%"')

root = tk.Tk()
root.title('Spotify Downloader')

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text='Digite o link da playlist:').grid(column=0, row=0)
entry = ttk.Entry(mainframe)
entry.grid(column=0, row=1)

log = tk.Text(mainframe, width=80, height=24, wrap='none')
log.grid(column=0, row=7)

def writeToLog(msg):
    numlines = int(log.index('end - 1 line').split('.')[0])
    log['state'] = 'normal'
    if numlines==24:
        log.delete(1.0, 2.0)
    if log.index('end-1c')!='1.0':
        log.insert('end', '\n')
    log.insert('end', msg)
    log['state'] = 'disabled'

def folder():
    global directory
    directory = filedialog.askdirectory(title="Escolha a pasta para salvar as músicas")
    root.update()
    ttk.Label(mainframe, text=directory).grid(column=0, row=2)

def downloader():
    source = entry.get()
    site = requests.get(source).content
    soup = BS(site, 'html.parser')
    lista = soup.find_all(class_="eWYxOj")
    length = 0
    pb1 = ttk.Progressbar(mainframe, orient='horizontal', length=500, mode='determinate')
    pb1.grid(column=0, row=6)
    mainframe.update
    for i in lista:
        length += 1
        ttk.Label(mainframe, text=f"Baixando {length} / {len(lista)}").grid(column=0, row=5)
        root.update()
        s = Search(f"Music {i.string} {i.find_next('a').string}")
        writeToLog(f'Baixando {s.results[0].title}')
        pb1['value'] += 50 / len(lista)
        try:
            stream = s.results[0].streams.get_by_itag(251)
        except AgeRestrictedError:
            print("Video com restrição de idade não foi baixado.")
            writeToLog("Video com restrição de idade não foi baixado.")
        else:
            stream.download(output_path=f"{directory}/{soup.find(class_='iJkkJW').string}")
            writeToLog(f'Convertendo {stream.default_filename} para MP3')
            AudioSegment.from_file(f"{directory}/{soup.find(class_='iJkkJW').string}/{stream.default_filename}").export(f"{directory}/{soup.find(class_='iJkkJW').string}/{stream.default_filename}.mp3", format="mp3")
            os.remove(f"{directory}/{soup.find(class_='iJkkJW').string}/{stream.default_filename}")
            writeToLog(f'{stream.default_filename} - Salvo com sucesso')
        pb1['value'] += 50 / len(lista)
    writeToLog('Playlist baixada com sucesso!')

def start():
    threading.Thread(target=downloader).start()

ttk.Button(mainframe, text="Escolher pasta", command=folder).grid(column=0, row=3)
ttk.Button(mainframe, text="Baixar", command=start).grid(column=0, row=4)

root.mainloop()