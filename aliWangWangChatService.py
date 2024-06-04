from flask import Flask
from flask import request
from flask_cors import CORS
import aliWangWangRx
import aliWangWangTx
import aliWangWangStoreInfo
import json

app = Flask('aliWangWang-Chat-Service')
CORS(app)


@app.route('/health', methods=['GET'])
def health_check():
    return "OK"


@app.route('/aliWangWang/tx', methods=['POST'])
def send_chat():
    data = request.get_json()

    aliWangWangTx.chatWithCustomer(data['offerId'], data['chatList'], data['userName'])

    return "SUCCESS"


@app.route('/aliWangWang/rx', methods=['POST'])
def recv_chat():
    data = json.loads(json.dumps(request.get_json()))

    return json.dumps(aliWangWangRx.getChatHistory(data['offerId'], data['userName']), default=lambda o: o.__dict__)


@app.route('/aliWangWang/store/info', methods=['POST'])
def get_store_info():
    data = request.get_json()

    return aliWangWangStoreInfo.getStoreInfo(data['offerId'], data['userName'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10015, debug=False)


