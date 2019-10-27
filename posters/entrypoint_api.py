from startup import create_app
import argparse

def cli():
    p = argparse.ArgumentParser()
    p.add_argument('--host', dest='host', default='localhost')
    p.add_argument('--port', dest='port', type=int, default=8000)
    p.add_argument('--debug', dest='debug', action='store_true')
    args = p.parse_args()
    app = create_app(debug=args.debug)
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    cli()
