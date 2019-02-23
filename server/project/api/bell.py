import os
import sys
import hashlib
import datetime

from flask import Blueprint, jsonify, request, render_template

from project.api.models import User, Profile, Asset, Provider
from project.api.models import user_profile, asset_profile, provider_profile
from project import db

from sqlalchemy import or_

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
        response.append(asset.to_json())
    
    return jsonify(response)


@bell_blueprint.route("/bell/alerts")
def bell_alerts():
    response = {
        "alertId": "2d4be346-120c-11e8-b642-0ed5f89f718b",
        "title": "Emergency Alert",
        "message": "Yo mamma so fat even penguins are jealous of the way she waddles."
    }
    return jsonify(response)


@bell_blueprint.route(
    "/bell/hidden/provider/<int:provider_id>/refreshRate", methods=["PUT"]
)
def bell_hidden_provider_refresh_rate(provider_id):
    response = {}
    request_json = request.get_json()
    if "refreshRateInSeconds" not in request_json:
        response["message"] = "Missing refreshRateInSeconds key in request body"
        return jsonify(response), 400
    provider = Provider.query.filter_by(provider_id=provider_id).first()
    provider.refresh_rate_in_seconds = request_json["refreshRateInSeconds"]
    db.session.commit()
    response["message"] = "Update successful"
    return jsonify(response)


@bell_blueprint.route("/bell/hidden/asset/<string:asset_id>", methods=["PUT"])
def bell_hidden_asset(asset_id):
    response = {}
    secret_key = request.headers.get("secretKey")
    request_json = request.get_json()

    # Validation
    if secret_key != os.environ["HEADER_SECRET_KEY"]:
        response["message"] = "Invalid header secret key"
        return jsonify(response), 401
    
    keys = ["providerId", "title", "licensingWindow", "profileIds", "media"]
    for key in keys:
        if key not in request_json:
            response["message"] = "Missing {} key in request body".format(key)
            return jsonify(response), 400

    provider_id = request_json["providerId"]
    provider = Provider.query.filter_by(provider_id=provider_id).first()
    if provider is None:
        response["message"] = "Invalid provider id"
        return jsonify(response), 404

    licensing_window = request_json["licensingWindow"]
    licensing_window_keys = ["start", "end"]
    for key in licensing_window_keys:
        if key not in licensing_window:
            response["message"] = "Missing licensingWindow {} key in request body".format(key)
            return jsonify(response), 400

    media = request_json["media"]
    media_keys = ["mediaId", "durationInSeconds"]
    for key in media_keys:
        if key not in request_json["media"]:
            response["message"] = "Missing media {} key in request body".format(key)
            return jsonify(response), 400

    # Update or create an asset
    media_id = media["mediaId"]
    asset = Asset.query.filter_by(media_id=media_id).first()
    create = False
    if asset is None:
        asset = Asset()
        create = True
    
    asset.media_id = media_id
    asset.title = request_json["title"]
    
    asset.provider_id = int(provider_id)
    asset.duration_in_seconds = media["durationInSeconds"]
    asset.licensing_window_start = licensing_window["start"]
    asset.licensing_window_end = licensing_window["end"]

    if (not create):
        asset.profiles = []
    for prof_id in request_json["profileIds"]:
        profile = Profile.query.filter_by(profile_id=prof_id).first()
        asset.profiles.append(profile)

    if create:
        db.session.add(asset)
        response["message"] = "Asset created successfully"
    else:
        response["message"] = "Asset updated successfully"
    db.session.commit()

    return jsonify(response)


@bell_blueprint.route("/bell/hidden/account", methods=["POST"])
def bell_hidden_account():
    response = {}
    secret_key = request.headers.get("secretKey")
    request_json = request.get_json()

    # Validation
    if secret_key != os.environ["HEADER_SECRET_KEY"]:
        response["message"] = "Invalid header secret key"
        return jsonify(response), 401

    keys = ["accountId", "profiles", "username", "password"]
    for key in keys:
        if key not in request_json:
            response["message"] = "Missing {} key in request body".format(key)
            return jsonify(response), 400

    profile_names = request_json["profiles"]
    for name in profile_names:
        profile = Profile.query.filter_by(name=name).first()
        if profile is None:
            response["message"] = "Invalid profile name: {}".format(name)
            return jsonify(response), 400

    user_id = request_json["accountId"]
    user = User.query.filter_by(user_id=user_id).first()
    if user is not None:
        response["message"] = "User already exists"
        return jsonify(response), 409

    user = User()
    user.user_id = user_id
    user.username = request_json["username"]
    password = request_json["password"].encode("utf-8")
    user.hashed_password = hashlib.sha256(password).hexdigest()
    for name in profile_names:
        profile = Profile.query.filter_by(name=name).first()
        user.profiles.append(profile)
    db.session.add(user)
    db.session.commit()
    response["message"] = "Account created successfully"
    return jsonify(response), 201


@bell_blueprint.route("/bell/search")
def bell_search():
    response = []
    search = f"%{request.args.get('query', '')}%"

    assets = (
        db.session
        .query(Asset)
        .join(Provider, Provider.provider_id == Asset.provider_id)
        .join(asset_profile, asset_profile.c.media_id == Asset.media_id)
        .join(
            provider_profile,
            provider_profile.c.provider_id == Provider.provider_id)
        .join(
            Profile,
            or_(
                Profile.profile_id == asset_profile.c.profile_id,
                Profile.profile_id == provider_profile.c.profile_id
            )
        )
        .filter(
            or_(
                Asset.title.ilike(search),
                Provider.name.ilike(search),
                Profile.name.ilike(search)
            )
        )
        .all()
    )

    for asset in assets:
        response.append(asset.to_json())

    return jsonify(response)
