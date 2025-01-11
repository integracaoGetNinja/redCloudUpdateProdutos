import pandas as pd
import base64
from pymongo import MongoClient
import os
import uuid
import requests
from datetime import datetime
import json

# > pyinstaller  spec.spec
# winclassbenicio@gmail.com
client = MongoClient(
    'mongodb+srv://henriquedb:Y2du8cnwhZYzjrlE@cluster0.vgf811c.mongodb.net/?retryWrites=true&w=majority')

db = client['db_produtos']
col = db['col_produtos']

col_clientes = db['col_clientes']
col_distribuidores = db['col_distribuidores']

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}


def atualizar_status_credito(tabela_excel):
    linha_inicial = 1
    df = pd.read_excel(tabela_excel, skiprows=range(1, linha_inicial))

    for indice, data in df.iterrows():
        idCredito = str(data.iloc[0])
        status = str(data.iloc[1])

        payload = json.dumps({
            "isCredito": True,
            "status": status
        })
        headers = {
            'Authorization': 'chave_api 32b19b99033db32ab955 aplicacao 120f779a-59dc-4351-92f6-857efd50362a',
            'Content-Type': 'application/json'
        }

        url = "http://191.252.178.129:5000/atualizar_status/" + idCredito

        requests.put(url, headers=headers, data=payload)
        print(idCredito, " ", status)

    print("Status das Solicitações de Crédito Atualizadas!")
    input("ok!")


def atualizar_status_produto(tabela_excel):
    linha_inicial = 1
    df = pd.read_excel(tabela_excel, skiprows=range(1, linha_inicial))

    for indice, data in df.iterrows():
        idPedido = str(data.iloc[0])
        status = str(data.iloc[1])

        payload = json.dumps({
            "isCredito": False,
            "status": status
        })
        headers = {
            'Authorization': 'chave_api 32b19b99033db32ab955 aplicacao 120f779a-59dc-4351-92f6-857efd50362a',
            'Content-Type': 'application/json'
        }

        url = "http://191.252.178.129:5000/atualizar_status/" + idPedido

        respost = requests.put(url, data=payload, headers=headers)
        print(respost.status_code)
        print(idPedido, " ", status)

    print("Status das Solicitações de Produtos Atualizados!")
    input("ok!")


def atualizar_distribuidores(tabela_excel):
    col_distribuidores.delete_many({})
    linha_inicial = 1

    df = pd.read_excel(tabela_excel, skiprows=range(1, linha_inicial))

    lista_dados = []
    for indice, data in df.iterrows():
        empresa = str(data.iloc[0])
        cidade = str(data.iloc[1])
        zonaEntrega = str(data.iloc[2])
        produtos = str(data.iloc[3])
        valorMinimo = str(data.iloc[4])
        frete = str(data.iloc[5])
        meioPagamento = str(data.iloc[6])
        prazo = str(data.iloc[7])
        fraquenciaAtualizacao = str(data.iloc[8])
        aceitaVouche = str(data.iloc[10])
        horarioCorte = str(data.iloc[11])
        obs = str(data.iloc[12])

        lista_dados.append({
            "_id": base64.b64encode(str(uuid.uuid4()).encode('utf-8')).decode('utf-8'),
            "empresa": empresa,
            "cidade": cidade,
            "zonaEntrega": zonaEntrega,
            "produtos": produtos,
            "valorMinimo": valorMinimo,
            "frete": frete,
            "meioPagamento": meioPagamento,
            "prazo": prazo,
            "fraquenciaAtualizacao": fraquenciaAtualizacao,
            "aceitaVouche": aceitaVouche,
            "horarioCorte": horarioCorte,
            "obs": obs
        })

        print(f"Distribuidor {indice} registrado!")

    print("Inserindo no banco de dados...")
    col_distribuidores.insert_many(lista_dados)
    print("Produtos atualizados no banco de dados!")
    input("ok!")


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
            "_id": base64.b64encode(str(uuid.uuid4()).encode('utf-8')).decode('utf-8'),
            "sku": sku,
            "estoque": estoque,
            "nome": nome,
            "preco": preco,
            "fornecedor": fornecedor
        })

    print("Inserindo no banco de dados...")
    col.insert_many(lista_dados)
    print("Produtos atualizados no banco de dados!")
    data_hora_atual = datetime.now()

    formato = "%Y-%m-%d %H:%M:%S"
    data_hora_formatada = data_hora_atual.strftime(formato)

    url_put = "http://191.252.178.129:5000/last_update"

    payload = json.dumps({
        "msg": data_hora_formatada
    })

    headers = {
        'Authorization': 'chave_api 32b19b99033db32ab955 aplicacao 120f779a-59dc-4351-92f6-857efd50362a',
        'Content-Type': 'application/json'
    }

    response = requests.post(url_put, data=payload, headers=headers)

    if response.status_code == 200:
        print(data_hora_formatada)
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

print("Versão 7.0")

clienteOrProduto = input(
    "Atualizar Clientes ( 1 )\nAtualizar Produtos ( 2 )\nAtualizar Distribuidores ( 3 )\nAtualizar Status Crédito ( 4 "
    ")\nAtualizar Status Produto ( 5 )\nR - ")

input(f"Foram reconhecidos {len(lista_arq)} arquivos de excel, escolha qual deve ser usado: ok!")
for arquivo in lista_arq:
    resposta = input(f"{arquivo} NÃO (1) ou SIM (2 ou ENTER): ")
    if resposta != "1":
        print("Atualizando, aguarde...")

        if clienteOrProduto == "1":
            atualizar_cliente(arquivo)
        elif clienteOrProduto == "2":
            atualizar_produtos(arquivo)
        elif clienteOrProduto == "3":
            atualizar_distribuidores(arquivo)
        elif clienteOrProduto == "4":
            atualizar_status_credito(arquivo)
        elif clienteOrProduto == "5":
            atualizar_status_produto(arquivo)
        break
