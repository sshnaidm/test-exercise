from flask import Flask


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    from testex.models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    from testex.controllers import api
    app.register_blueprint(api)

    return app
