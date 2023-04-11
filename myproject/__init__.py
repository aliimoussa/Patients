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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alimoussa:7iDSkjEpzJAAmhoeAgdJxIalHCSu2l4o@dpg-cgot0c8u9tun42r5lfvg-a.frankfurt-postgres.render.com/healthcare_4ko1'

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