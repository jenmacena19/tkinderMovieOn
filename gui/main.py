
from tkinter import *
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

janela = Tk()
janela.title("MovieOn System")

lb = Label(janela, text="Resultado")
lb.place(x=100, y=200)

ed1 = Entry(janela)
ed1.place(x=100, y=100)
ed2 = Entry(janela)
ed2.place(x=100, y=130)

base = carregaMovieLens()

def teste():
    user1 = ed1.get()
    lb['text'] = user1
    return lb

def euclidiana():
    si = {} #verifica se há simaliridade
    user1 = ed1.get()
    user2 = ed2.get()
    for item in base[user1]:
        #verificar todas os filmes que o usuario 1 viu e dps ver se o user 2 viu tb
        if item in base[user2]:
            si[item] = 1
        if len(si) == 0: return 00,
        soma  = sum([pow(base[user1][item] - base[user2][item], 2)
                     for item in base[user1] if item in base[user2]])
        return 1/(1 + sqrt(soma))

def getRecomendacoes():
    user = ed1.get()
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

bt = Button(master=janela, text="Recomendar", width=50, command=getRecomendacoes)
bt.place(x=100, y=150)

janela.geometry("862x519")
janela.mainloop()

