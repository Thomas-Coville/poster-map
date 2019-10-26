# inspired from https://github.com/GoogleCloudPlatform/getting-started-python/tree/master/optional-kubernetes-engine

import os
import logging
import datetime
import json

# Flask extensions
from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow

from webargs import fields
from webargs.flaskparser import use_args

# Domain modules
import config
from models import Job, JobSchema


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
    MongoEngine(app)
    Marshmallow(app)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)


    # API
    @app.route('/jobs', methods = ['POST'])
    @use_args(JobSchema())
    def create_job(args):
        job = Job(
            latitude =args["latitude"],
            longitude = args["longitude"],
            width = args["width"],
            height = args["height"],
            zoom = args["zoom"]
        ).save()

        schema = JobSchema()
        return schema.dump(job)
        
    @app.route('/health')
    def health_check():
        return 'ok', 200

    # Return validation errors as JSON
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return jsonify({"errors": messages}), err.code, headers
        else:
            return jsonify({"errors": messages}), err.code

    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app
