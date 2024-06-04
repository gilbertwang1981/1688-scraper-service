from flask import Flask
from flask import request
from flask_cors import CORS
import json
import SourcingProduct

app = Flask('aliWangWang-Chat-Service')
CORS(app)


@app.route('/health', methods=['GET'])
def health_check():
    return "OK"


@app.route('/sourcing/create', methods=['POST'])
def create_sourcing():
    SourcingProduct.publishSourcing()

    return "SUCCESS"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10016, debug=False)


