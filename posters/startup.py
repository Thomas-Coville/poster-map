import os
import logging
import datetime
import json

# Flask extensions
from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from dynaconf import FlaskDynaconf, settings
import tasks
import jobs

logger = logging.getLogger()

def create_app(debug=False):
    return entrypoint(debug=debug, mode='app')

def create_celery(debug=False):
    return entrypoint(debug=debug, mode='celery')

def entrypoint(debug=False, mode='app'):
    assert isinstance(mode, str), 'bad mode type "{}"'.format(type(mode))
    assert mode in ('app','celery'), 'bad mode "{}"'.format(mode)

    app = Flask('posters')    
    configure_app(app)

    # Extensions
    MongoEngine(app)
    Marshmallow(app)

    app.debug = debug

    configure_logging(debug=debug)

    # register blueprints
    app.register_blueprint(jobs.bp, url_prefix='')

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

    @app.route('/health')
    def health_check():
        return 'ok', 200


    configure_celery(app, tasks.celery)

    if mode=='app':
        return app
    elif mode=='celery':
        return tasks.celery

def configure_app(app):

    logger.info('configuring flask app')
    FlaskDynaconf(app)

def configure_celery(app, celery):

    # set broker url and result backend from app config
    celery.conf.broker_url = settings['CELERY_BROKER_URL']
    celery.conf.result_backend = settings['CELERY_RESULT_BACKEND']

    celery.conf.update(app.config)

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    celery.finalize()

    return celery

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
