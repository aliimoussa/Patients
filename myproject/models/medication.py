from ..extensions import db
from ..models.patient import Patient


class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    patient = db.relationship(Patient, backref='medications')
    name = db.Column(db.String(100))
    dosage = db.Column(db.Float(50))
    frequency = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
