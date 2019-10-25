# inspired from https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/

import os
import logging

from flask import Flask


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

   
    # Create a health check handler. Health checks are used when running on
    # Google Compute Engine by the load balancer to determine which instances
    # can serve traffic. Google App Engine also uses health checking, but
    # accepts any non-500 response as healthy.
    @app.route('/health')
    def health_check():
        return 'ok', 200

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app