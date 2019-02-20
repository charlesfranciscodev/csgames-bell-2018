from project import db


user_profile = db.Table("user_profile",
    db.Column(
        "user_id", db.String(36),
        db.ForeignKey("user.user_id"), primary_key=True
    ),
    db.Column(
        "profile_id", db.Integer,
        db.ForeignKey("profile.profile_id"), primary_key=True
    )
)

asset_profile = db.Table("asset_profile",
    db.Column(
        "media_id", db.String(11),
        db.ForeignKey("asset.media_id"), primary_key=True
    ),
    db.Column(
        "profile_id", db.Integer,
        db.ForeignKey("profile.profile_id"), primary_key=True
    )
)

provider_profile = db.Table("provider_profile",
    db.Column(
        "provider_id", db.Integer,
        db.ForeignKey("provider.provider_id"), primary_key=True
    ),
    db.Column(
        "profile_id", db.Integer,
        db.ForeignKey("profile.profile_id"), primary_key=True
    )
)


class User(db.Model):
    user_id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(64), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    profiles = db.relationship(
        "Profile", secondary=user_profile lazy="subquery",
        backref=db.backref("profiles", lazy=True)
    )

    def __init__(self, user_id, username, hashed_password, birthdate, profiles):
        self.user_id = user_id
        self.username = username
        self.hashed_password = hashed_password
        self.birthdate = birthdate
        self.profiles = profiles


class Profile(db.Model):
    profile_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, profile_id, name):
        self.profile_id = profile_id
        self.name = name


class Asset(db.Model):
    media_id = db.Column(db.String(11), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    profiles = db.relationship(
        "Profile", secondary=asset_profile lazy="subquery",
        backref=db.backref("profiles", lazy=True)
    )
    provider_id = db.Column(
        db.Integer, db.ForeignKey("provider_id"), nullable=False
    )
    duration_in_seconds = db.Column(db.Integer, nullable=False)
    licensing_window_start = db.Column(db.DateTime, nullable=False)
    licensing_window_end = db.Column(db.DateTime, nullable=False)


class Provider(db.Model):
    refresh_rate_in_seconds = db.Column(db.Integer, nullable=False)
    profiles = db.relationship(
        "Profile", secondary=provider_profile lazy="subquery",
        backref=db.backref("profiles", lazy=True)
    )
    provider_id = db.Column(db.Integer, primary_key=True)

    assets = db.relationship("Asset", backref="provider")
