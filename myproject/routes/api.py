from datetime import date, timedelta, datetime

from flask import Blueprint
from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy import or_, cast, Date
from sqlalchemy.sql.functions import coalesce

from myproject.decorators import transactional
from myproject.error_handling import InvalidCSVFileError
from myproject.models import Medication, Patient
from myproject.schemas.schemas import PatientSchema, MedicationSchema
from myproject.utils import upload_data

api_bp = Blueprint('api', __name__, url_prefix='/api')


class PatientList(Resource):
    def post(self):
        selected_age = 0
        data = request.get_json()
        if 'age' in data and data.get('age').strip():
            selected_age = int(data.get('age'))
        column_name = data.get('column_name')

        search_param = data.get('search')
        sort_order = request.args.get('sort_order', 'desc')

        page = data.get('page', 1)

        per_page = data.get('per_page', 10)
        search_term = f'%{search_param}%'

        patient_schema = PatientSchema(many=True)
        # initialize result
        results = Patient.query
        if selected_age:
            # calculate dob based on selected age
            dob = datetime.now() - timedelta(days=365 * selected_age)
            dob_date = dob.date()  # extract date from datetime object
            print(f"dob={dob_date}")
            results = results.filter(
                cast(Patient.date_of_birth, Date) <= dob_date)

        # sort
        if column_name:
            if sort_order == 'asc':
                results = results.order_by(getattr(Patient, column_name).asc())
            else:
                results = results.order_by(getattr(Patient, column_name).desc())

        # filter
        if search_param:
            results = results.filter(
                or_(Patient.first_name.ilike(search_term),
                    Patient.last_name.ilike(search_term),
                    Patient.address.ilike(search_term),
                    Patient.phone_number.ilike(search_term),
                    Patient.insurance_plan.ilike(search_term))
            )

        if results:
            results = results.paginate(page=page, per_page=per_page, error_out=False)

            return jsonify({
                'error': False,
                'message': 'All Patients',
                'data': patient_schema.dump(results.items),
                'total_pages': results.pages,
                'total_items': results.total
            })


@api_bp.route('/patients/<int:patient_id>/medications', methods=['get'])
def patient_medications(patient_id):
    print("medications")
    medications = Medication.query.filter_by(patient_id=patient_id).all()

    if not medications:
        return jsonify({
            'error': True,
            'message': f'No medications found for patient ID: {patient_id}',
            'data': []
        })

    medications_schema = MedicationSchema(many=True)
    serialized_data = medications_schema.dump(medications)
    return jsonify({
        'error': False,
        'message': f'Successfully retrieved medications for patient {patient_id}',
        'data': serialized_data
    })


@transactional
@api_bp.route('/upload_csv', methods=['POST'])
def upload_csv_data():
    if 'file' not in request.files:
        return jsonify({
            'error': True,
            'message': 'No File Uploaded',
            'data': []
        })

    file = request.files['file']

    # Check if the file is a CSV
    if file.filename.split('.')[-1] != 'csv':
        return jsonify({
            'error': True,
            'message': 'Only csv file are supported',
            'data': []
        })
    try:
        file = request.files['file']
        result = upload_data(file)
        return jsonify(result), 200
    except InvalidCSVFileError as e:
        return jsonify({
            'error': True,
            'message': str(e),
            'data': []
        }), 400