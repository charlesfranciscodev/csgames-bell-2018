import sys, hashlib
import datetime

from flask import Blueprint, jsonify, request, render_template

from project.api.models import User, Profile, Asset, Provider
from project.api.models import user_profile, asset_profile, provider_profile
from project import db

bell_blueprint = Blueprint("bell", __name__, template_folder="./templates")


@bell_blueprint.route("/app/ping")
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong"
    })


@bell_blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bell_blueprint.route("/bell/authentication", methods=["POST", "PUT"])
def bell_authentication():
    response = {}
    request_json = request.get_json()
    if request.method == "POST":
        username = request_json["username"]
        password = request_json["password"].encode("utf-8")
        user_object = User.query.filter_by(username=username).first()
        if user_object is None:
            response["message"] = "Invalid username or password"
            return jsonify(response), 401
        hashed_password = hashlib.sha256(password).hexdigest()
        if hashed_password != user_object.hashed_password:
            response["message"] = "Invalid username or password"
            return jsonify(response), 401
    elif request.method == "PUT":
        hashed_credentials = request_json["hashedCredentials"].split(":")
        username = hashed_credentials[0]
        hashed_password = hashed_credentials[1]
        user_object = User.query.filter_by(username=username).first()
        if user_object is None:
            response["message"] = "Invalid username or password"
            return jsonify(response), 401
        user_object.hashed_password = hashed_password
        db.session.commit()

    response["accountId"] = user_object.user_id
    response["profiles"] = []
    for profile in user_object.profiles:
        response["profiles"].append(profile.name)
    response["hashedCredentials"] = username + ":" + hashed_password
    return jsonify(response)


@bell_blueprint.route("/bell/assets")
def bell_assets():
    response = []
    profile_names = request.args.getlist("profiles")
    current = datetime.datetime.utcnow()
    assets = (
        db.session
        .query(Asset)
        .filter(
            Asset.profiles.any(Profile.name.in_(profile_names)),
            Asset.licensing_window_start <= current,
            Asset.licensing_window_end >= current,
        )
        .all()
    )

    for asset in assets:
        provider =  Provider.query.filter_by(
            provider_id=asset.provider_id).first()
        asset_dict = {
            "title": asset.title,
            "providerId": provider.name,
            "refreshRateInSeconds": provider.refresh_rate_in_seconds,
            "media": {
                "mediaId": asset.media_id,
                "durationInSeconds": asset.duration_in_seconds
            }
        }
        response.append(asset_dict)
    
    return jsonify(response)


@bell_blueprint.route("/bell/alerts")
def bell_alerts():
    response = {
        "alertId": "2d4be346-120c-11e8-b642-0ed5f89f718b",
        "title": "Emergency Alert",
        "message": "Yo mamma so fat even penguins are jealous of the way she waddles."
    }
    return jsonify(response)
