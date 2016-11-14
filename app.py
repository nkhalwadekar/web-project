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
    from models.user import User

    incoming_json = request.get_json(force=True)

    if incoming_json is None:
        return abort(404)

    username = incoming_json.get("username")

    user = User.query.filter_by(username=username).first()

    if user is None:
        user = User(username)
        db.session.add(user)
        db.session.commit()

    # Create the Model
    m = Message(user.id, incoming_json.get("input", ""))

    # save it to the database
    db.session.add(m)
    db.session.commit()

    response = {
        "result": "ok"
    }

    return jsonify(response)


@app.route("/messages/<username>", methods=['GET'])
def get_user_messages(username):
    from models.message import Message
    from models.user import User

    user = User.query.filter_by(username=username).first()

    if user is None:
        return abort(404)

    messages = Message.query.filter_by(user_id=user.id).all()

    results = []
    for message in messages:
        results.append(message.to_dict())

    response = {
        "results": results
    }

    return jsonify(response)


@app.route("/messages/<message_id>/replies", methods=['POST'])
def create_reply(message_id):
    from models.message import Message
    from models.user import User

    incoming_json = request.get_json(force=True)

    if incoming_json is None:
        return abort(404)

    username = incoming_json.get("username")

    user = User.query.filter_by(username=username).first()

    if user is None:
        user = User(username)
        db.session.add(user)
        db.session.commit()

    # Create the Model
    m = Reply(user.id, message_id, incoming_json.get("input", ""))

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
