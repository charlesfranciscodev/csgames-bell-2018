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
    __tablename__ = "user"
    user_id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(64), nullable=False)
    birthdate = db.Column(db.DateTime)
    profiles = db.relationship(
        "Profile", secondary=user_profile, lazy="subquery",
        backref=db.backref("user_profiles", lazy=True)
    )


class Profile(db.Model):
    __tablename__ = "profile"
    profile_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class Asset(db.Model):
    __tablename__ = "asset"
    media_id = db.Column(db.String(11), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    profiles = db.relationship(
        "Profile", secondary=asset_profile, lazy="subquery",
        backref=db.backref("asset_profiles", lazy=True)
    )
    provider_id = db.Column(
        db.Integer, db.ForeignKey("provider.provider_id"), nullable=False
    )
    duration_in_seconds = db.Column(db.Integer, nullable=False)
    licensing_window_start = db.Column(db.DateTime, nullable=False)
    licensing_window_end = db.Column(db.DateTime, nullable=False)


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
