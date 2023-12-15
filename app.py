import pandas as pd
import base64
from pymongo import MongoClient
import os

client = MongoClient(
    'mongodb+srv://henriquedb:Y2du8cnwhZYzjrlE@cluster0.vgf811c.mongodb.net/?retryWrites=true&w=majority')
db = client['db_produtos']
col = db['col_produtos']

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}


def atualizar_banco(tabela_excel):
    col.delete_many({})

    linha_inicial = 7

    df = pd.read_excel(tabela_excel, skiprows=range(1, linha_inicial))

    lista_dados = []
    for indice, data in df.iterrows():
        sku = data.iloc[2]
        lista_dados.append({
            "_id": base64.b64encode(sku.encode('utf-8')).decode('utf-8'),
            "sku": sku,
            "estoque": data.iloc[9],
            "nome": data.iloc[3],
            "preco": data.iloc[13]
        })

    col.insert_many(lista_dados)
    print("Produtos atualizados no banco de dados!")
    input("ok!")


arquivos = os.listdir()

lista_arq = []
for arquivo in arquivos:
    ex_arquivo = arquivo.split(".")

    if len(ex_arquivo) > 1:
        if ex_arquivo[1] in ALLOWED_EXTENSIONS:
            lista_arq.append(arquivo)

input(f"Foram reconhecidos {len(lista_arq)} arquivos de excel, escolha qual deve ser usado: ok!")
for arquivo in lista_arq:
    resposta = int(input(f"{arquivo} SIM (1) ou não (2): "))
    if resposta == 1:
        print("Atualizando, aguarde...")
        atualizar_banco(arquivo)

