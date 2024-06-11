from flask import Flask
from flask import request
from flask import jsonify
import ProductDetailScrapy
from flask_cors import CORS

app = Flask('crawl-service')
CORS(app)


@app.route('/health', methods=['GET'])
def health_check():
    return "OK"


@app.route('/1688/get_detail_from_1688', methods=['GET'])
def get_detail_from_1688():
    productId = request.args.get('id')

    url = 'https://detail.1688.com/offer/' + productId + '.html?spm=a26352.13672862.offerlist.59.2fac1e62cO65Hm' \
                                                          '&cosite=-&tracelog=p4p&_p_isad=1&' \
                                                          'clickid=fcf11b87a6f14ad796969a9a52836c9b&' \
                                                          'sessionid=a659238081d473668bf0881d132d92ee'

    return jsonify(vars(ProductDetailScrapy.crawl_from_1688(url, 'tq02h2a_gb1981')))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10012, debug=False)


