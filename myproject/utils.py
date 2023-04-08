from datetime import date

import pandas as pd

from myproject.models import Patient, Medication
from .extensions import db


def upload_data(file):
    patient_header = {'first_name', 'last_name', 'date_of_birth', 'address', 'phone_number', 'email',
                      'treatment_plan'}
    medication_header = {'phone_number', 'name', 'dosage', 'frequency', 'start_date', 'end_date'}
    df = pd.read_csv(file)
    cleaned_df = clean_csv_data(df)
    print(cleaned_df.columns)
    df = cleaned_df.rename(columns=lambda x: x.strip())
    actual_headers = set(df.columns)

    if patient_header.issubset(actual_headers):
        insert_patients_from_csv(df)
    elif medication_header.issubset(actual_headers):
        insert_medication(df)


def insert_medication(df):
    # Get all the phone numbers of patients from the database
    patient_numbers = [phone[0] for phone in Patient.query.with_entities(Patient.phone_number).all()]

    print(f"phone_numbers: {patient_numbers}")
    medications = []
    for index, row in df.iterrows():
        # Get the patient object from the database
        if str(row['phone_number']).strip() in patient_numbers:
            patient = Patient.query.filter_by(phone_number=str(row['phone_number']).strip()).first()
            if not patient:
                # Handle the case where the phone number doesn't exist in the patient table
                print(f"Medication with phone number {row['phone_number']} doesn't have a matching patient record.")
                continue

            # Check if a medication record already exists for this patient and medication
            existing_medication = Medication.query.filter_by(
                name=row['name'],
                dosage=row['dosage'],
                frequency=row['frequency'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                patient_id=patient.id
            ).first()

            if existing_medication:
                # Handle the case where the medication record already exists
                # todo log
                print(f"Medication record already exists for patient with phone number {row['phone_number']}.")
                continue

            # Create a new medication object
            medication = Medication(
                name=row['name'],
                dosage=row['dosage'],
                frequency=row['frequency'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                patient_id=patient.id
            )
            medications.append(medication)
        # Add the medication to the database
        else:
            # Handle the case where the phone number doesn't exist in the patient table
            print(f"Medication with phone number {row['phone_number']} doesn't have a matching patient record.")
        db.session.add_all(medications)
        db.session.commit()


def insert_patients_from_csv(df):
    def validate_row(row):
        # Check that all required columns are present
        required_columns = ['first_name', 'last_name', 'date_of_birth', 'address', 'phone_number', 'email']
        missing_columns = set(required_columns) - set(row.index)
        if missing_columns:
            raise ValueError(f"Missing columns: {', '.join(missing_columns)}")

        # Check that the date_of_birth column is a valid date
        if not pd.to_datetime(row['date_of_birth'], errors='coerce'):
            raise ValueError(f"Invalid date_of_birth value: {row['date_of_birth']}")

    patients = []
    # Iterate over each row of the CSV file
    for index, row in df.iterrows():
        # Validate the data for the row
        try:
            validate_row(row)
        except ValueError as e:
            print(f"Skipping row {index + 1}: {e}")
            continue

        # Check if the phone number already exists in the database
        if Patient.query.filter_by(phone_number=str(row['phone_number'])).first():
            print(f"Skipping row {index + 1}: phone number {row['phone_number']} already exists in database")
            continue

        # Create a new Patient object with the data from the CSV file
        patient = Patient(first_name=row['first_name'],
                          last_name=row['last_name'],
                          date_of_birth=row['date_of_birth'],
                          address=row['address'],
                          phone_number=row['phone_number'],
                          email=row['email'],
                          insurance_plan=row['insurance_plan'],
                          treatment_plan=row['treatment_plan']

                          )
        patients.append(patient)
    # Add the Patient object to the database
    db.session.add_all(patients)
    db.session.commit()


def clean_csv_data(df):
    # Remove any leading/trailing whitespace from column names and values
    df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
    # Remove any rows with missing or invalid data
    df = df.dropna(how='any')
    # Convert date columns to datetime objects
    date_columns = ['date_of_birth', 'start_date', 'end_date']
    # Check that the date_of_birth column is a valid date
    for column in date_columns:
        if column in df.columns:
            df.loc[:, column] = pd.to_datetime(df[column])
    return df


def calculate_age(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return age


# aggregation function
def aggregate_medications_by_frequency():
    medication_frequency = Medication.query.with_entities(Medication.frequency, db.func.count()).group_by(
        Medication.frequency).all()
    return medication_frequency


def aggregate_medication_dosages():
    """
    Aggregates medication dosages by patient ID and returns a dictionary with the total dosage for each patient.
    """
    medication_dosages = Medication.query.with_entities(Medication.patient_id, Medication.dosage).all()
    dosage_totals = {}
    for patient_id, dosage, in medication_dosages:
        if patient_id not in dosage_totals:
            dosage_totals[patient_id] = 0
        dosage_totals[patient_id] += int(dosage)
    return dosage_totals
