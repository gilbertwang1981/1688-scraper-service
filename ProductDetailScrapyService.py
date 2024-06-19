from flask import Flask
from flask import request
from flask import jsonify
import ProductDetailScrapy
from flask_cors import CORS

app = Flask('1688-product-service')
CORS(app)


@app.route('/health', methods=['GET'])
def health_check():
    return "OK"


@app.route('/1688/get_detail_from_1688', methods=['GET'])
def get_detail_from_1688():
    userName = request.args.get('userName')
    offerId = request.args.get('offerId')

    url = 'https://detail.1688.com/offer/' + offerId + '.html'

    return jsonify(vars(ProductDetailScrapy.crawl_from_1688(url, userName)))


@app.route('/product/cookie/update/<string:userName>', methods=['POST'])
def update_ali_cookie(userName):
    data = request.get_json()

    return ProductDetailScrapy.updateCookie(userName, data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10012, debug=False)


