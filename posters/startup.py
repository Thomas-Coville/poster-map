# inspired from https://github.com/GoogleCloudPlatform/getting-started-python/tree/master/optional-kubernetes-engine

import os
import logging
import datetime
import json

# Flask extensions
from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow

# Domain modules
import config
from models import Job


def create_app(config_overrides=None):
    app = Flask(__name__)

    # config
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    if config_overrides is not None:
        app.config.update(config_overrides)

    # Extensions
    mongo = MongoEngine(app)
    marshmallow = Marshmallow(app)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)


    # API
    @app.route('/jobs', methods = ['POST'])
    def create_job():
        job = Job(width=1234).save()
        print(job.dump())

        return 'ok', 200

    @app.route('/health')
    def health_check():
        return 'ok', 200

    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app
