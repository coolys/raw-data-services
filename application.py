import flask
from flask import Flask, jsonify
import happybase
import uuid

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

connection = happybase.Connection(app.config['HBASE_HOST'])
feeds_table = connection.table('feeds')


@app.route('/api/v1/feeds', methods=['GET'])
def get_all_feeds():
    results = []
    for key, data in feeds_table.scan():
        item = {'id': key, 'title': data['meta:title'], 'description': data['meta:description'],
                'thumb': data['meta:thumb']}
        results.append(item)
    return jsonify({'result': results})


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'Request not found !'}), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'message': 'Internal server error !'}), 500


@app.route('/api/v1/feeds', methods=['POST'])
def add_feed():
    json_data = request.get_json()
    feed_id = str(uuid.uuid1().time)
    feeds_table.put(feed_id, {b'meta:title': json_data['title'],
                              b'meta:description': json_data['description'], b'meta:thumb': json_data['thumb']})
    json_data['id'] = feed_id
    return jsonify(json_data)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'api': 'feed services', 'version': 'v1.0'})


@app.route('/api/v1/insert', methods=['GET'])
def insert():
    for n in range(1, 100):
        feed_id = str(uuid.uuid1().time)
        feeds_table.put(feed_id,
                        {b'meta:title': 'hello title ' + str(n), b'meta:description': 'hello description ' + str(n),
                         b'meta:thumb': 'hello-thumb-' + str(n)})
    return jsonify({'api': 'feed services', 'version': 'v1.0'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, threaded=True)
