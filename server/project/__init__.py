import os

from flask import Flask
from flask_cors import CORS

from project.api.bell import bell_blueprint

cors = CORS()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    cors.init_app(app)

    # register blueprints
    app.register_blueprint(bell_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app}

    return app
