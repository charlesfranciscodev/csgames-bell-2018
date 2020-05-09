import datetime
import jwt

from flask import current_app
from project import db

user_profile = db.Table(
    "user_profile",
    db.Column(
        "user_id", db.String(36),
        db.ForeignKey(
            "user.user_id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        primary_key=True
    ),
    db.Column(
        "profile_id", db.Integer,
        db.ForeignKey(
            "profile.profile_id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        primary_key=True
    )
)

asset_profile = db.Table(
    "asset_profile",
    db.Column(
        "media_id", db.String(11),
        db.ForeignKey(
            "asset.media_id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        primary_key=True,
    ),
    db.Column(
        "profile_id", db.Integer,
        db.ForeignKey(
            "profile.profile_id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        primary_key=True
    )
)

provider_profile = db.Table(
    "provider_profile",
    db.Column(
        "provider_id", db.Integer,
        db.ForeignKey(
            "provider.provider_id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        primary_key=True
    ),
    db.Column(
        "profile_id", db.Integer,
        db.ForeignKey(
            "profile.profile_id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        primary_key=True
    )
)


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(64), nullable=False)
    birthdate = db.Column(db.DateTime)
    profiles = db.relationship(
        "Profile", secondary=user_profile, lazy="subquery",
        backref=db.backref("user_profiles", lazy=True)
    )

    def to_json(self):
        user_dict = {
            "accountId": self.user_id,
            "profiles": [],
            "hashedCredentials": self.username + ":" + self.hashed_password
        }
        for profile in self.profiles:
            user_dict["profiles"].append(profile.name)
        return user_dict

    def encode_auth_token(self):
        """Generates the auth token"""
        now = datetime.datetime.utcnow()
        delta = datetime.timedelta(
            days=current_app.config.get("TOKEN_EXPIRATION_DAYS"),
            seconds=current_app.config.get("TOKEN_EXPIRATION_SECONDS")
        )
        try:
            payload = {
                "exp": now + delta,
                "iat": now,
                "sub": self.user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get("SECRET_KEY"),
                algorithm="HS256"
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the auth token"""
        try:
            payload = jwt.decode(
                auth_token,
                current_app.config.get("SECRET_KEY")
            )
            return (True, payload["sub"])
        except jwt.ExpiredSignatureError:
            return (False, "Signature expired. Please log in again.")
        except jwt.InvalidTokenError:
            return (False, "Invalid token. Please log in again.")


class Profile(db.Model):
    __tablename__ = "profile"
    profile_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def to_json(self):
        profile_dict = {
            "profileId": self.profile_id,
            "name": self.name
        }
        return profile_dict


class Asset(db.Model):
    __tablename__ = "asset"
    media_id = db.Column(db.String(11), primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    profiles = db.relationship(
        "Profile", secondary=asset_profile, lazy="subquery",
        backref=db.backref("asset_profiles", lazy=True)
    )
    provider_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "provider.provider_id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        nullable=False
    )
    duration_in_seconds = db.Column(db.Integer, nullable=False)
    licensing_window_start = db.Column(db.DateTime, nullable=False)
    licensing_window_end = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        provider = Provider.query.filter_by(
            provider_id=self.provider_id).first()
        asset_dict = {
            "title": self.title,
            "provider": provider.provider_id,
            "providerId": provider.name,
            "refreshRateInSeconds": provider.refresh_rate_in_seconds,
            "media": {
                "mediaId": self.media_id,
                "durationInSeconds": self.duration_in_seconds
            },
            "licensingWindow": {
                "start": self.licensing_window_start.isoformat(),
                "end": self.licensing_window_end.isoformat()
            },
            "profileIds": [str(profile.profile_id) for profile in self.profiles]
        }
        return asset_dict


class Provider(db.Model):
    __tablename__ = "provider"
    refresh_rate_in_seconds = db.Column(db.Integer, nullable=False)
    profiles = db.relationship(
        "Profile", secondary=provider_profile, lazy="subquery",
        backref=db.backref("provider_profiles", lazy=True)
    )
    provider_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    assets = db.relationship("Asset", backref="provider")

    def to_json(self):
        provider_dict = {
            "providerId": self.provider_id,
            "name": self.name
        }
        return provider_dict
