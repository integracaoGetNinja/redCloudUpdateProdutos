from flask import Flask, render_template, request, redirect
import pandas as pd
import base64
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://henriquedb:Y2du8cnwhZYzjrlE@cluster0.vgf811c.mongodb.net/?retryWrites=true&w=majority')
db = client['db_produtos']
col = db['col_produtos']


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    col.delete_many({})

    linha_inicial = 2

    tabela_excel = request.files['file']

    df = pd.read_excel(tabela_excel, skiprows=range(1, linha_inicial))

    lista_dados = []
    for indice, data in df.iterrows():
        sku = str(data.iloc[2])
        print(f"Produto {indice} registrado!")
        lista_dados.append({
            "_id": base64.b64encode(sku.encode('utf-8')).decode('utf-8'),
            "sku": sku,
            "estoque": data.iloc[9],
            "nome": data.iloc[3],
            "preco": data.iloc[12]
        })
    col.insert_many(lista_dados)

    return "Produtos atualizados no banco de dados!"


if __name__ == "__main__":
    app.run(debug=True)
