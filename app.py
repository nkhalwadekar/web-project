from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/nehakhalwadekar/Desktop/work/web-project/db.db'
db = SQLAlchemy(app)

CORS(app)


@app.route("/echo", methods=['POST', 'GET'])
def echo():
    incoming_json = request.get_json(force=True)

    if incoming_json is None:
        return abort(404)

    return jsonify(incoming_json)


@app.route("/messages", methods=['POST'])
def create_message():
    from models.message import Message

    incoming_json = request.get_json(force=True)

    if incoming_json is None:
        return abort(404)

    # Create the Model
    m = Message(incoming_json.get("user_id", None), incoming_json.get("input", ""))

    # save it to the database
    db.session.add(m)
    db.session.commit()

    response = {
        "result": "ok"
    }

    return jsonify(response)

if __name__ == "__main__":
    #app.run(debug=True, ssl_context='adhoc')
    app.run(debug=True)
