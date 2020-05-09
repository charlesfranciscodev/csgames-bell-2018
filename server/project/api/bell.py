import os
import hashlib
import datetime
import dateutil.parser

from functools import wraps

from flask import Blueprint, jsonify, request

from project.api.models import User, Profile, Asset, Provider
from project.api.models import asset_profile, provider_profile
from project import db

from sqlalchemy import or_

bell_blueprint = Blueprint("bell", __name__)


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = {
            "message": "Provide a valid auth token."
        }
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify(response), 403
        auth_token = auth_header.split(" ")[1]
        valid_token, value = User.decode_auth_token(auth_token)
        if not valid_token:
            response["message"] = value
            return jsonify(response), 401
        user = User.query.filter_by(user_id=value).first()
        if user is None:
            return jsonify(response), 401
        return f(value, *args, **kwargs)
    return decorated_function


def optional_authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return f(None, *args, **kwargs)
        auth_token = auth_header.split(" ")[1]
        valid_token, value = User.decode_auth_token(auth_token)
        if not valid_token:
            return f(None, *args, **kwargs)
        user = User.query.filter_by(user_id=value).first()
        if user is None:
            return f(None, *args, **kwargs)
        return f(value, *args, **kwargs)
    return decorated_function


@bell_blueprint.route("/bell/authentication", methods=["POST"])
def bell_authentication_post():
    """Login for user(s)"""
    response = {}
    request_json = request.get_json()

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

    # Generate auth token
    auth_token = user_object.encode_auth_token()
    response = user_object.to_json()
    response["token"] = auth_token.decode()
    return jsonify(response)


@bell_blueprint.route("/bell/authentication", methods=["PUT"])
@authenticate
def bell_authentication_put(user_id):
    response = {}
    request_json = request.get_json()

    user_object = User.query.filter_by(user_id=user_id).first()

    if user_object is None:
        response["message"] = "User not found"
        return jsonify(response), 401

    hashed_credentials = request_json["hashedCredentials"].split(":")
    username = hashed_credentials[0]
    hashed_password = hashed_credentials[1]
    user_object.username = username
    user_object.hashed_password = hashed_password
    db.session.commit()

    return jsonify(user_object.to_json())


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


@bell_blueprint.route("/bell/hidden/asset/<string:media_id>", methods=["POST", "PUT"])
def bell_hidden_asset(media_id):
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

    licensing_window_start = licensing_window["start"]
    licensing_window_end = licensing_window["end"]
    licensing_window_start_datetime = dateutil.parser.parse(licensing_window_start)
    licensing_window_end_datetime = dateutil.parser.parse(licensing_window_end)
    if licensing_window_start_datetime > licensing_window_end_datetime:
        response["message"] = "Invalid licensing window"
        return jsonify(response), 400

    # Update or create an asset
    asset = Asset.query.filter_by(media_id=media_id).first()
    create = request.method == "POST"
    if create:
        if asset is None:
            asset = Asset()
            create = True
        else:
            message = "Asset {} already exists".format(media["mediaId"])
            response["message"] = message
            return jsonify(response), 400
    elif asset is None:
        message = "Asset {} does not exist".format(media["mediaId"])
        response["message"] = message
        return jsonify(response), 400

    asset.media_id = media["mediaId"]
    asset.title = request_json["title"]

    asset.provider_id = int(provider_id)
    asset.duration_in_seconds = media["durationInSeconds"]
    asset.licensing_window_start = licensing_window_start
    asset.licensing_window_end = licensing_window_end

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
    """Creates a user account"""
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

    username = request_json["username"]
    user = User.query.filter_by(username=username).first()
    if user is not None:
        response["message"] = "Username already exists"
        return jsonify(response), 409

    # Create user
    user = User()
    user.user_id = request_json["accountId"]
    user.username = username
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


@bell_blueprint.route("/bell/asset/<string:media_id>")
@optional_authenticate
def bell_asset(user_id, media_id):
    response = {}
    current = datetime.datetime.utcnow()

    # filter asset based on media_id and licensing window
    asset = (
        db.session
        .query(Asset)
        .filter(
            Asset.media_id == media_id,
            Asset.licensing_window_start <= current,
            Asset.licensing_window_end >= current
        )
        .first()
    )
    if asset is None:
        response["message"] = "Invalid media id or licensing window"
        return jsonify(response), 400

    # select currently logged in user
    if not user_id:
        return jsonify(asset.to_json())
    user = User.query.filter_by(user_id=user_id).first()

    # select asset provider
    provider = (
        db.session.query(Provider)
        .filter(Provider.provider_id == asset.provider_id)
        .first()
    )

    # filter by asset and provider profiles
    user_profiles = frozenset(user.profiles)
    if user_profiles.isdisjoint(asset.profiles):
        response["message"] = "Invalid asset profiles"
        return jsonify(response), 400

    if user_profiles.isdisjoint(provider.profiles):
        response["message"] = "Invalid provider profiles"
        return jsonify(response), 400

    return jsonify(asset.to_json())


@bell_blueprint.route("/bell/logout", methods=["POST"])
def bell_logout():
    response = {
        "message": "Logout successful"
    }

    return jsonify(response)


@bell_blueprint.route("/bell/profiles")
def bell_profiles():
    profiles = Profile.query.all()
    response = [profile.to_json() for profile in profiles]
    return jsonify(response)


@bell_blueprint.route("/bell/providers")
def bell_providers():
    providers = Provider.query.all()
    response = [provider.to_json() for provider in providers]
    return jsonify(response)
