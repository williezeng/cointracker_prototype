from flask import Flask, request, jsonify, Response

import constants

app = Flask(__name__)
from wallet_controller import WalletController


@app.route("/balance", methods=['POST'])
def balance_endpoint():
    data = request.get_json(force=True)
    required_fields = ['userid', 'btc_address']
    for field in required_fields:
        if field not in data:
            raise Exception("There's a missing field '{0}' in request".format(field))
    wallet_obj = WalletController(data['userid'])
    balance = wallet_obj.get_balance(data['btc_address'])
    return jsonify(balance), 200


@app.route("/transactions", methods=['POST'])
def transactions_endpoint():
    data = request.get_json(force=True)
    required_fields = ['userid', 'btc_address']
    for field in required_fields:
        if field not in data:
            raise Exception("There's a missing field '{0}' in request".format(field))
    wallet_obj = WalletController(data['userid'])
    def generate():
        for row in wallet_obj.get_transactions(data['btc_address']):
            yield row + '\n'
    return Response(generate(),  mimetype='application/json')


@app.route("/delete", methods=['POST'])
def delete_endpoint():
    data = request.get_json(force=True)
    required_fields = ['userid', 'btc_address']
    for field in required_fields:
        if field not in data:
            raise Exception("There's a missing field '{0}' in request".format(field))
    wallet_obj = WalletController(data['userid'])
    wallet_obj.remove_address_from_both_databases(data['btc_address'])
    return ('', 204)


@app.route("/add", methods=['POST'])
def add_endpoint():
    data = request.get_json(force=True)
    required_fields = ['userid', 'btc_address']
    for field in required_fields:
        if field not in data:
            raise Exception("There's a missing field '{0}' in request".format(field))
    wallet_obj = WalletController(data['userid'])
    wallet_obj.add_address(data['btc_address'])
    return ('', 204)

@app.route("/synch", methods=['POST'])
def synch_endpoint():
    data = request.get_json(force=True)
    required_fields = ['userid', 'btc_address']
    for field in required_fields:
        if field not in data:
            raise Exception("There's a missing field '{0}' in request".format(field))
    wallet_obj = WalletController(data['userid'])
    what = wallet_obj.synch_one_user_id()
    print(what)
    return ('', 204)

if __name__ == '__main__':
    app.run(host=constants.HTTP_ADDRESS, port=constants.HTTP_PORT)
