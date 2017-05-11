from flask import Flask


def create_app(config_filename):
    """
    Factory for flask application
    :param config_filename: name of configuration file
    :return: application object
    """
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    from testex.models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    from testex.controllers import api
    app.register_blueprint(api)

    return app
