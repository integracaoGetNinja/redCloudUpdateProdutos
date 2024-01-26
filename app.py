import pandas as pd
import base64
from pymongo import MongoClient
import os
import uuid

# > pyinstaller  spec.spec
# winclassbenicio@gmail.com
client = MongoClient(
    'mongodb+srv://henriquedb:Y2du8cnwhZYzjrlE@cluster0.vgf811c.mongodb.net/?retryWrites=true&w=majority')

db = client['db_produtos']
col = db['col_produtos']

col_clientes = db['col_clientes']

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}


def atualizar_produtos(tabela_excel):
    col.delete_many({})

    linha_inicial = 2

    df = pd.read_excel(tabela_excel, skiprows=range(1, linha_inicial))

    lista_dados = []
    for indice, data in df.iterrows():
        sku = str(data.iloc[2])
        estoque = data.iloc[8]
        nome = data.iloc[3]
        preco = data.iloc[12]
        fornecedor = data.iloc[1]

        if str(estoque).lower() == "nan":
            estoque = 0.0

        if str(nome).lower() == "nan":
            nome = ""

        if str(preco).lower() == "nan":
            preco = 0.0

        if str(fornecedor).lower() == "nan":
            fornecedor = ""

        print(f"Produto {indice} registrado!")

        lista_dados.append({
            "_id": base64.b64encode(sku.encode('utf-8')).decode('utf-8'),
            "sku": sku,
            "estoque": estoque,
            "nome": nome,
            "preco": preco,
            "fornecedor": fornecedor
        })

    print("Inserindo no banco de dados...")
    col.insert_many(lista_dados)
    print("Produtos atualizados no banco de dados!")
    input("ok!")


def atualizar_cliente(tabela_excel):
    col_clientes.delete_many({})

    linha_inicial = 2

    df = pd.read_excel(tabela_excel, skiprows=range(1, linha_inicial))

    lista_dados = []
    for indice, data in df.iterrows():
        nomeEstabelecimento = data.iloc[0]
        nomeCliente = data.iloc[1]
        sobreNome = data.iloc[2]
        enderecoEnglish = data.iloc[3]
        endereco = data.iloc[4]
        cidade = data.iloc[5]
        regiao = data.iloc[6]
        cep = data.iloc[7]
        telefone = data.iloc[8]
        email = data.iloc[9]
        cnpj = data.iloc[10]

        if str(nomeEstabelecimento).lower() == "nan":
            nomeEstabelecimento = ""

        if str(nomeCliente).lower() == "nan":
            nomeCliente = ""

        if str(sobreNome).lower() == "nan":
            sobreNome = ""

        if str(enderecoEnglish).lower() == "nan":
            enderecoEnglish = ""

        if str(endereco).lower() == "nan":
            endereco = ""

        if str(cidade).lower() == "nan":
            cidade = ""
        if str(regiao).lower() == "nan":
            regiao = ""

        if str(cep).lower() == "nan":
            cep = ""

        if str(telefone).lower() == "nan":
            telefone = ""

        if str(email).lower() == "nan":
            email = ""

        if str(cnpj).lower() == "nan":
            cnpj = ""

        print(f"Produto {indice} registrado!")

        lista_dados.append({
            "_id": base64.b64encode(str(uuid.uuid4()).encode('utf-8')).decode('utf-8'),
            "nomeEstabelecimento": nomeEstabelecimento,
            "nomeCliente": nomeCliente,
            "sobreNome": sobreNome,
            "enderecoEnglish": enderecoEnglish,
            "endereco": endereco,
            "cidade": cidade,
            "regiao": regiao,
            "cep": cep,
            "telefone": telefone,
            "email": email,
            "cnpj": cnpj
        })

    print("Inserindo no banco de dados...")
    col_clientes.insert_many(lista_dados)
    print("Clientes atualizados no banco de dados!")
    input("ok!")


arquivos = os.listdir()

lista_arq = []
for arquivo in arquivos:
    ex_arquivo = arquivo.split(".")

    if len(ex_arquivo) > 1:
        if ex_arquivo[1] in ALLOWED_EXTENSIONS:
            lista_arq.append(arquivo)

print("Versão 4.0 - Updates -> https://pastebin.com/Ef9CUMcW ")
clienteOrProduto = input("Atualizar Clientes ( 1 )  -  Atualizar Produtos ( 2 ou ENTER ): ")
input(f"Foram reconhecidos {len(lista_arq)} arquivos de excel, escolha qual deve ser usado: ok!")
for arquivo in lista_arq:
    resposta = input(f"{arquivo} NÃO (1) ou SIM (2 ou ENTER): ")
    if resposta != "1":
        print("Atualizando, aguarde...")

        if clienteOrProduto == "1":
            atualizar_cliente(arquivo)
        else:
            atualizar_produtos(arquivo)
        break
