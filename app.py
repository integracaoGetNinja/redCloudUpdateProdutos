import pandas as pd
import base64
from pymongo import MongoClient
import os

# > pyinstaller  spec.spec
client = MongoClient(
    'mongodb+srv://henriquedb:Y2du8cnwhZYzjrlE@cluster0.vgf811c.mongodb.net/?retryWrites=true&w=majority')
db = client['db_produtos']
col = db['col_produtos']

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}


def atualizar_banco(tabela_excel):
    col.delete_many({})

    linha_inicial = 2

    df = pd.read_excel(tabela_excel, skiprows=range(1, linha_inicial))

    lista_dados = []
    for indice, data in df.iterrows():
        sku = str(data.iloc[2])
        estoque = data.iloc[9]
        nome = data.iloc[3]
        preco = data.iloc[12]

        if str(estoque).lower() == "nan":
            estoque = 0.0

        if str(nome).lower() == "nan":
            nome = ""

        if str(preco).lower() == "nan":
            preco = 0.0

        print(f"Produto {indice} registrado!")

        lista_dados.append({
            "_id": base64.b64encode(sku.encode('utf-8')).decode('utf-8'),
            "sku": sku,
            "estoque": estoque,
            "nome": nome,
            "preco": preco
        })

    print("Inserindo no banco de dados...")
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

print("Versão 2.0 - Correção de valores nulos")
input(f"Foram reconhecidos {len(lista_arq)} arquivos de excel, escolha qual deve ser usado: ok!")
for arquivo in lista_arq:
    resposta = int(input(f"{arquivo} SIM (1) ou não (2): "))
    if resposta == 1:
        print("Atualizando, aguarde...")
        atualizar_banco(arquivo)
