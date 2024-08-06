from flask import Flask
from without_index import without_index_bp
from with_index import with_index_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(without_index_bp, url_prefix='/without-index')
    app.register_blueprint(with_index_bp, url_prefix='/with-index')

    # Define a default route
    @app.route('/')
    def hello_world():
        return 'hello world'

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=9000)
