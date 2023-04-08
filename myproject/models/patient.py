from sqlalchemy import Index
from sqlalchemy import func, text

from ..extensions import db


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.DateTime)
    address = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))

    insurance_plan = db.Column(db.String(100))
    treatment_plan = db.Column(db.String(100))
