import webbrowser
import re
import sys
import os
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from pathlib import Path
from math import sqrt

#carregar dados da base de dados Movie Lens
def carregaMovieLens(path='C:\ml-100k'):
    filmes = {}
    for linha in open(path + '/u.item'):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo
    #print(filmes)

    base = {}
    for linha in open(path + '/u.data'):
        (usuario, idfilme, nota, tempo) = linha.split('\t')
        base.setdefault(usuario, {})
        base[usuario][filmes[idfilme]] = float(nota)
    return base

# Add tkdesigner to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from tkdesigner.designer import Designer
except ModuleNotFoundError:
    raise RuntimeError("Couldn't add tkdesigner to the PATH.")


# Path to asset files for this GUI window.
ASSETS_PATH = Path(__file__).resolve().parent / "assets"

# Required in order to add data files to Windows executable
path = getattr(sys, '_MEIPASS', os.getcwd())
os.chdir(path)

output_path = ""

base = carregaMovieLens()

def euclidiana():
    si = {} #verifica se há simaliridade
    user1 = token_entry.get()
    user2 = URL_entry.get()
    for item in base[user1]:
        #verificar todas as musicas que o usuario 1 viu e dps ver se o user 2 viu tb
        if item in base[user2]:
            si[item] = 1
        if len(si) == 0: return 00,
        soma  = sum([pow(base[user1][item] - base[user2][item], 2)
                     for item in base[user1] if item in base[user2]])
        return 1/(1 + sqrt(soma))

def getRecomendacoes():
    user = token_entry.get()
    totais = {}
    somaSimilaridade = {}
    for outro in base:
        if outro == user:
            continue
        similaridade = euclidiana()
        float(similaridade)
        if similaridade <= 0:
            continue

        for item in base[outro]:
            if item not in base[user]:
                totais.setdefault(item, 0)
                totais[item] += base[outro][item] * similaridade
                somaSimilaridade.setdefault(item, 0)
                somaSimilaridade[item] += similaridade
    rankings=[(total / somaSimilaridade[item], item) for item, total in totais.items()]
    rankings.sort()
    rankings.reverse()
    lb['text'] = rankings
    return lb

def btn_clicked():
    token = token_entry.get()
    output_path = path_entry.get()
    output_path = output_path.strip()

    if not token:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Por favor, insira os dados.")
        return

    if not output_path:
        tk.messagebox.showerror(
            title="Invalid Path!", message="Enter a valid USER.")
        return

    tk.messagebox.showinfo(
        "Success!", f"Project successfully generated at {token} user.")


def select_path():
    global output_path

    output_path = tk.filedialog.askdirectory()
    '''path_entry.delete(0, tk.END)
    path_entry.insert(0, output_path)'''


def know_more_clicked(event):
    instructions = (
        "https://github.com/jenmacena19/tkinderMovieOn")
    webbrowser.open_new_tab(instructions)


def make_label(master, x, y, h, w, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0)  # don't shrink
    f.place(x=x, y=y)

    label = tk.Label(f, *args, **kwargs)
    label.pack(fill=tk.BOTH, expand=1)

    return label


window = tk.Tk()

lb = tk.Label(window, text="Label1")
lb.place(x=490, y=200)

logo = tk.PhotoImage(file=ASSETS_PATH / "iconbitmap.gif")
window.call('wm', 'iconphoto', window._w, logo)
window.title("MovieOn System")

window.geometry("862x519")
window.configure(bg="#0D0437")
canvas = tk.Canvas(
    window, bg="#0D0437", height=519, width=862,
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FFFFFF", outline="",)
canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill="#FFFFFF", outline="")

text_box_bg = tk.PhotoImage(file=ASSETS_PATH / "TextBox_Bg.png")
token_entry_img = canvas.create_image(650.5, 167.5, image=text_box_bg)
URL_entry_img = canvas.create_image(650.5, 248.5, image=text_box_bg)
filePath_entry_img = canvas.create_image(650.5, 329.5, image=text_box_bg)


token_entry = tk.Entry(bd=0, bg="#F2F0FC", highlightthickness=0)
token_entry.place(x=490.0, y=137+25, width=321.0, height=35)
token_entry.focus()

URL_entry = tk.Entry(bd=0, bg="#F2F0FC", highlightthickness=0)
URL_entry.place(x=490.0, y=218+25, width=321.0, height=35)

path_entry = tk.Entry(bd=0, bg="#F2F0FC", highlightthickness=0)
path_entry.place(x=490.0, y=299+25, width=321.0, height=35)


path_picker_img = tk.PhotoImage(file = ASSETS_PATH / "path_picker.png")
path_picker_button = tk.Button(
    image = path_picker_img,
    text = '',
    compound = 'center',
    fg = 'black',
    borderwidth = 0,
    highlightthickness = 0,
    command = select_path,
    relief = 'flat')

path_picker_button.place(
    x = 780, y = 315,
    width = 24,
    height = 22)

canvas.create_text(
    490.0, 156.0, text="ID Amigo 1", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    490.0, 315.5, text="Base de Dados", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    490.0, 234.5, text="ID Amigo 2",
    fill="#515486", font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    646.5, 428.5, text="Buscar",
    fill="#FFFFFF", font=("Arial-BoldMT", int(13.0)))
canvas.create_text(
    605, 88.0, text="Veja um filme sugerido \n pelos amigos!",
    fill="#0D0437", font=("Arial-BoldMT", int(18.0)))

title = tk.Label(
    text="Bem-vindo ao MovieOn", bg="#0D0437",
    fg="#AD22F1", font=("Arial-BoldMT", int(22.0)))
title.place(x=27.0, y=120.0)

info_text = tk.Label(
    text="Este é um sistema desenvolvido para \n"
    "recomendar seus filmes favoritos.\n"
    "Aqui você pode:\n\n"

    "- Ver os filmes favoritos dos seus amigos\n"
    "- Ver filmes mais recomendados, \n desde os clássicos!\n"
    "- Acesso a uma grande variedade de filmes\n"
    "- Ver avaliações dos seus amigos\n",
    bg="#0D0437", fg="white", justify="left",
    font=("Georgia", int(14.0)))

info_text.place(x=27.0, y=200.0)

know_more = tk.Label(
    text="Click para mais informações!",
    bg="#0D0437", fg="#AD22F1", cursor="hand2")
know_more.place(x=27, y=420)
know_more.bind('<Button-1>', know_more_clicked)

generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / "generate.png")
generate_btn = tk.Button(
    image=generate_btn_img, borderwidth=0, highlightthickness=0,
    command=getRecomendacoes, relief="flat")
generate_btn.place(x=557, y=401, width=180, height=55)

window.resizable(False, False)
window.mainloop()
