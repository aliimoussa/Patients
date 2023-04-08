from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aiia:aiia2020@localhost:5432/health'
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
