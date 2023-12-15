from flask import Flask, jsonify
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://henriquedb:Y2du8cnwhZYzjrlE@cluster0.vgf811c.mongodb.net/?retryWrites=true&w=majority')
db = client['db_produtos']
col = db['col_produtos']

app = Flask(__name__)


@app.route("/produtos")
def produtos():
    return jsonify([x for x in col.find({})])


if __name__ == "__main__":
    app.run()
