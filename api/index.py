from flask import Flask, jsonify, request, send_file
from pymongo import MongoClient
import gridfs
from bson import objectid

client = MongoClient(
    'mongodb+srv://henriquedb:Y2du8cnwhZYzjrlE@cluster0.vgf811c.mongodb.net/?retryWrites=true&w=majority')
db = client['db_produtos']
col = db['col_produtos']

clientImages = MongoClient('mongodb://195.200.6.225:27017/')
db_images = clientImages['db_images']
col_images = db_images['product_images']
fs = gridfs.GridFS(db_images)

col_clientes = db['col_clientes']
col_distribuidores = db['col_distribuidores']

app = Flask(__name__)


@app.route("/distribuidores")
def distribuidores():
    return jsonify([x for x in col_distribuidores.find({})])


@app.route('/get/imagem/produto/<img_id>')
def serve_image(img_id):
    try:
        file = fs.get(objectid.ObjectId(img_id))
        return send_file(file, mimetype='image/png')  # Mimetype pode variar conforme a imagem
    except Exception as e:
        return str(e), 404


@app.route('/get/imagem/produto')
def get_image_product():
    sku = request.args.get('sku')
    image_payload = col_images.find_one({'sku': sku})

    if image_payload:
        return jsonify({
            "img": image_payload.get('img')
        })
    else:
        return jsonify({
            "img": 'https://i.imgur.com/kdlBSiV.png'
        })


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
