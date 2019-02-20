class BaseConfig:
    """Base configuration"""
    TESTING = False
    SECRET_KEY = "9a39bf1d2039ceab910f5905149e74a0"


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
