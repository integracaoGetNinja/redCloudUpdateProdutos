from flask import Flask, jsonify
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://henriquedb:Y2du8cnwhZYzjrlE@cluster0.vgf811c.mongodb.net/?retryWrites=true&w=majority')
db = client['db_produtos']
col = db['col_produtos']

col_clientes = db['col_clientes']
col_distribuidores = db['col_distribuidores']

app = Flask(__name__)


@app.route("/distribuidores")
def distribuidores():
    return jsonify([x for x in col_distribuidores.find({})])


@app.route("/produtos")
def produtos():
    return jsonify([x for x in col.find({})])


@app.route("/clientes")
def clientes():
    return jsonify([x for x in col_clientes.find({})])


if __name__ == "__main__":
    app.run()
