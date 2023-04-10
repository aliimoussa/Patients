from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
# todo must be removed
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://alimoussa:7iDSkjEpzJAAmhoeAgdJxIalHCSu2l4o@dpg-cgot0c8u9tun42r5lfvg-a.frankfurt-postgres.render.com/healthcare_4ko1'

db = SQLAlchemy(app)


def transactional(func):
    def wrapper(*args, **kwargs):
        try:
            db.session.begin_nested()
            response = func(*args, **kwargs)
            db.session.commit()
            return response
        except SQLAlchemyError as e:
            db.session.rollback()
            return str(e), 500

    return wrapper
