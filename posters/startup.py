# inspired from https://github.com/GoogleCloudPlatform/getting-started-python/tree/master/optional-kubernetes-engine

import os
import logging
import datetime
import json

# Flask extensions
from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from dynaconf import FlaskDynaconf, settings

from webargs import fields
from webargs.flaskparser import use_args

# Domain modules
from models import JobSchema
from services import JobsService
import tasks


logger = logging.getLogger()

def create_app(debug=False):
    return entrypoint(debug=debug, mode='app')

def create_celery(debug=False):
    return entrypoint(debug=debug, mode='celery')

def entrypoint(debug=False, mode='app'):
    assert isinstance(mode, str), 'bad mode type "{}"'.format(type(mode))
    assert mode in ('app','celery'), 'bad mode "{}"'.format(mode)

    app = Flask(__name__)    
    configure_app(app)

    # Extensions
    MongoEngine(app)
    Marshmallow(app)

    app.debug = debug

    configure_logging(debug=debug)
    configure_celery(app, tasks.celery)

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


    if mode=='app':
        return app
    elif mode=='celery':
        return tasks.celery

def configure_app(app):

    logger.info('configuring flask app')
    FlaskDynaconf(app)

def configure_celery(app, celery):

    # set broker url and result backend from app config
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']

    # subclass task base for app context
    # http://flask.pocoo.org/docs/0.12/patterns/celery/
    TaskBase = celery.Task
    class AppContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = AppContextTask

    # run finalize to process decorated tasks
    celery.finalize()

def configure_logging(debug=False):

    root = logging.getLogger()
    h = logging.StreamHandler()
    fmt = logging.Formatter(
        fmt='%(asctime)s %(levelname)s (%(name)s) %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )
    h.setFormatter(fmt)

    root.addHandler(h)

    if debug:
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)