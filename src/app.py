from flask import Flask

from config import config
from config.routes import metrics_api


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    with app.app_context():
        from src.metrics.core.persistence.models import db
        db.init_app(app)

    # API blueprints
    app.register_blueprint(metrics_api)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
