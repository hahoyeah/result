from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb적어주기', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/result", methods=["POST"])
def result_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    result_list = list(db.result.find({}, {'_id': False}))
    count = len(result_list)+1 # 개수에 따라 1씩 늘려준다.

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'num': count,
        'done': 0
    }
    db.result.insert_one(doc)

    return jsonify({'msg':'등록했다구리!'})

@app.route("/result/done", methods=["POST"])
def result_done():
    num_receive = request.form['num_give']
    db.result.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '삭제 완료!'})

@app.route("/result", methods=["GET"])
def result_get():
    comment_list = list(db.result.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
