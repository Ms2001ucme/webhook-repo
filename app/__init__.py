from flask import Flask, render_template
from app.extensions import mongo
from app.webhook import webhook_bp  # import the Blueprint
from .logging_config import configure_logging

def create_app():
    """
    Application factory function to create and configure the Flask app instance.

    Configures:
    - MongoDB connection via PyMongo
    - Logging setup using `logging_config.configure_logging`
    - Registers webhook blueprint
    - Adds a home route rendering 'index.html'

    Returns:
        Flask app instance
    """
    app = Flask(__name__)

    configure_logging(app)

    app.config["MONGO_URI"] = "mongodb://localhost:27017/webhookDB"
    mongo.init_app(app)

    # Register blueprint
    app.register_blueprint(webhook_bp)

    @app.route('/')
    def home():
        """
        Root route of the application that renders the home page.

        Returns:
            Rendered HTML template 'index.html'
        """
        return render_template("index.html")

    return app
