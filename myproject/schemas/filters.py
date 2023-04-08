import datetime
from datetime import date

from marshmallow import Schema, validates, ValidationError, validates_schema
from marshmallow import fields

from myproject.models import Patient


class AgeFilterSchema(Schema):
    from_age = fields.Integer(required=True)
    to_age = fields.Integer(required=True)

    @validates('from_age')
    def validate_from_age(self, value):
        if value < 0:
            raise ValidationError('from_age must be a positive integer')

    @validates('to_age')
    def validate_to_age(self, value):
        if value < 0:
            raise ValidationError('to_age must be a positive integer')

    @validates('to_age')
    def validate_age_range(self, value, data):
        if value < data['from_age']:
            raise ValidationError('to_age must be greater than or equal to from_age')


class PatientFilterSchema(Schema):
    search = fields.String()
    from_age = fields.String()
    to_age = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    date_of_birth = fields.Date()
    phone_number = fields.String()
    insurance_plan = fields.String()

    class Meta:
        model = Patient

    @validates_schema
    def validate(self, data, **kwargs):
        age_filter = {}
        print(data)
        if 'from_age' in data and 'to_age' in data:
            from_age = data.pop('from_age')
            to_age = data.pop('to_age')
            if from_age == '' and to_age == '':
                age_filter = None
            else:
                age_filter['min_age'] = from_age
                age_filter['max_age'] = to_age

            if from_age > to_age:
                response_data = {
                    "error": True,
                    "message": "From Age cannot be greater than To Age",
                    "data": []
                }
                return response_data

            patients = Patient.query.filter(Patient.first_name == 'John')
        if age_filter:
            query = Patient.query.filter(18 <= int(age_filter['max_age'])) \
                .filter(40 >= int(age_filter['min_age'])) \
                .filter_by(**data)
            filtered_data = query.all()
            return filtered_data
        return patients


from datetime import datetime, date


def calculate_age(date_of_birth):
    if isinstance(date_of_birth, str):
        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()

    today = date.today()
    dob_date = date(date_of_birth.year, date_of_birth.month, date_of_birth.day)
    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    return int(age)
