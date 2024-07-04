import aliImageSearch
from flask import request
from flask import Flask
from flask_cors import CORS

app = Flask('1688-search-service')
CORS(app)


@app.route('/health', methods=['GET'])
def health_check():
    return "OK"


@app.route('/image/search', methods=['POST'])
def search():
    data = request.get_json()

    aliImageSearch.downloadImage(data['imageUrl'])

    targets = aliImageSearch.aliSearch()

    return targets


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10018, debug=False)


