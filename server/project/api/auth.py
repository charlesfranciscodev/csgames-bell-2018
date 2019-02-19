import sys, json, hashlib

from flask import Blueprint, jsonify, request, render_template, session, abort
from flask import current_app as app

auth_blueprint = Blueprint("auth", __name__, template_folder="./templates")


def get_auth_data():
    if "auth" in session and session["auth"] is not None:
        return session["auth"]
    with app.open_resource("authentication.json") as f:
        users = json.load(f)
        for user in users:
            del user["password"]
        session["auth"] = users


def get_profile_data():
    if "auth" not in session or session["auth"] is None:
        get_auth_data()
    # TODO


@auth_blueprint.route("/app/ping")
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong"
    })


@auth_blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def get_user(username):
    users = get_auth_data()
    for user in users:
        if user["username"] == username:
            return user
    return None


def update_user_password(username, hashed_password):
    users = get_auth_data()
    for user in users:
        if user["username"] == username:
            user["hashedPassword"] = hashed_password
            session["auth"] = users
            break


@auth_blueprint.route("/bell/authentication", methods=["POST", "PUT"])
def bell_authentication():
    response = {}
    request_json = request.get_json()
    if request.method == "POST":
        username = request_json["username"]
        password = request_json["password"].encode("utf-8")
        users = get_auth_data()
        user_object = get_user(username)
        
        if user_object is None:
            response["message"] = "Invalid username or password"
            return jsonify(response), 401
        hashed_password = hashlib.sha256(password).hexdigest()
        if hashed_password != user_object["hashedPassword"]:
            response["message"] = "Invalid username or password"
            return jsonify(response), 401
    elif request.method == "PUT":
        hashed_credentials = request_json["hashedCredentials"].split(":")
        username = hashed_credentials[0]
        hashed_password = hashed_credentials[1]
        user_object = get_user(username)
        if user_object is None:
            response["message"] = "Invalid username or password"
            return jsonify(response), 401
        update_user_password(username, hashed_password)

    response["accountId"] = user_object["id"]
    response["profiles"] = []
    for profile in user_object["profiles"]:
        response["profiles"].append(profile["name"])
    response["hashedCredentials"] = username + ":" + hashed_password
    return jsonify(response)
