# inspired from https://github.com/GoogleCloudPlatform/getting-started-python/tree/master/optional-kubernetes-engine

import os
import logging
import datetime
import json

# Flask extensions
from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from dynaconf import FlaskDynaconf

from webargs import fields
from webargs.flaskparser import use_args

# Domain modules
from models import JobSchema
from services import JobsService


def create_app():
    app = Flask(__name__)

    FlaskDynaconf(app)    

    # Extensions
    MongoEngine(app)
    Marshmallow(app)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # API
    @app.route('/jobs', methods=['POST'])
    @use_args(JobSchema())
    def create_job(args):

        job = JobsService.create_job( latitude=args["latitude"],
            longitude=args["longitude"])

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
