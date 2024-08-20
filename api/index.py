from flask import Flask, jsonify, request
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
    try:
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 1000))
        produtos = list(col.find({}).skip(offset).limit(limit))

        total_count = col.count_documents({})

        return jsonify({
            'total': total_count,
            'produtos': produtos
        })
    except Exception as e:
        return jsonify({'error': str(e)}),


@app.route("/clientes")
def clientes():
    return jsonify([x for x in col_clientes.find({})])


if __name__ == "__main__":
    app.run()
