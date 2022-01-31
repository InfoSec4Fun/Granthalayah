# standard imports
# external imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# internal imports
from atheneum.config import Config

# definition of objects
db         = SQLAlchemy()


def create_app():
    """
       This function defines and  create's a instance of the application 
    """
    # definition of app
    app    = Flask(__name__)
    app.config.from_object(Config) 

    # initiating
    db.init_app(app)

    # registration of apps
    from atheneum.requisite.routes import requisite
    app.register_blueprint(requisite)

    return app