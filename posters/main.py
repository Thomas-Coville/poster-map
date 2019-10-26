
import startup
import config


# Note: debug=True is enabled here to help with troubleshooting. You should
# remove this in production.
app = startup.create_app(config, debug=True)


# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
