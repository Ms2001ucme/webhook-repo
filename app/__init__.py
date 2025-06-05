from flask import Flask, render_template
from app.extensions import mongo
from app.webhook import webhook_bp  # import the Blueprint

def create_app():
    app = Flask(__name__)

    app.config["MONGO_URI"] = "mongodb://localhost:27017/webhookDB"
    mongo.init_app(app)

    # Register blueprint
    app.register_blueprint(webhook_bp)

    @app.route('/')
    def home():
        return render_template("index.html")

    return app
