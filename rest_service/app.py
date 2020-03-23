import logging
from os import getenv

import connexion


def create_app():
    app = connexion.FlaskApp(__name__, specification_dir='openapi/')
    app.add_api('api.yaml')

    app.app.logger.setLevel(getenv('LOG_LEVEL', logging.INFO))
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
