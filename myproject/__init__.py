from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api

from .extensions import db, migrate
from .routes.analysis import analysis_bp
from .routes.api import api_bp, PatientList
from .routes.index import index_bp

ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    api_rest = Api(app)

    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aiia:aiia2020@localhost:5432/health'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alimoussa:1mIGrEOxxZJC0WpFZ0G0Z5ezyUmPMwNS@dpg-cgk17o8rddleuds86vv0-a.frankfurt-postgres.render.com/healthcare_3eih'
    #
    # database_url= 'postgresql://alimoussa:1mIGrEOxxZJC0WpFZ0G0Z5ezyUmPMwNS@dpg-cgk17o8rddleuds86vv0-a.frankfurt-postgres.render.com/healthcare_3eih'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    migrate.init_app(app, db)

    app.register_blueprint(index_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(analysis_bp)

    api_rest.add_resource(PatientList, '/patients')
    app.debug = True
    return app
