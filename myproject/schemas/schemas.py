from flask import Flask
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from myproject.models import Medication, Patient

app = Flask(__name__)

ma = Marshmallow(app)


# Define your serialization schemas
class MedicationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Medication


class PatientSchema(SQLAlchemyAutoSchema):
    medications = fields.Nested(MedicationSchema(), many=True)

    class Meta:
        model = Patient



