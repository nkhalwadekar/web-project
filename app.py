from flask import Flask, request, jsonify, abort
app = Flask(__name__)

@app.route("/echo", methods=['POST', 'GET'])
def echo():
    incoming_json = request.get_json()

    if incoming_json is None:
        return abort(404)

    return jsonify(incoming_json)

if __name__ == "__main__":
    app.run()
