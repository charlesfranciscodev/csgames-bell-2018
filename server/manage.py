import json
import dateutil.parser

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User, Profile, Asset, Provider

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    db.reflect()
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    """Seeds the database."""
    with open("authentication.json") as f:
        users = json.load(f)
        for user in users:
            user_object = User()
            user_object.user_id = user["id"]
            user_object.username = user["username"]
            user_object.hashed_password = user["hashedPassword"]
            user_object.birthdate = dateutil.parser.parse(user["birthdate"])
            for profile in user["profiles"]:
                profile_id = int(profile["id"])
                obj = Profile.query.filter_by(profile_id=profile_id).first()
                if not obj:
                    obj = Profile()
                    obj.profile_id = profile_id
                    obj.name = profile["name"]
                user_object.profiles.append(obj)
            db.session.add(user_object)

    with open("programming.json") as f:
        dictionary = json.load(f)
        assets = dictionary["assets"]
        providers = dictionary["providers"]
        for provider in providers:
            obj = Provider()
            obj.refresh_rate_in_seconds = provider["refreshRateInSeconds"]
            obj.provider_id = provider["id"]
            obj.name = provider["name"]
            for prof_id in provider["profileIds"]:
                profile = Profile.query.filter_by(profile_id=prof_id).first()
                obj.profiles.append(profile)
            db.session.add(obj)

        for asset in assets:
            asset_object = Asset()
            asset_object.media_id = asset["mediaId"]
            asset_object.title = asset["title"]
            asset_object.provider_id = asset["providerId"]
            asset_object.duration_in_seconds = asset["durationInSeconds"]
            asset_object.licensing_window_start = dateutil.parser.parse(
                asset["licensingWindow"]["start"]
            )
            asset_object.licensing_window_end = dateutil.parser.parse(
                asset["licensingWindow"]["end"]
            )
            for prof_id in asset["profileIds"]:
                profile = Profile.query.filter_by(profile_id=prof_id).first()
                asset_object.profiles.append(profile)
            db.session.add(asset_object)

    db.session.commit()


if __name__ == "__main__":
    cli()
