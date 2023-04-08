import io
import base64
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Blueprint, render_template
from flask import jsonify

from myproject.models import Patient
from myproject.utils import calculate_age, aggregate_medications_by_frequency, aggregate_medication_dosages

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')


@analysis_bp.route('/age_analysis', methods=['GET'])
def age_analysis():
    patients = Patient.query.all()
    age_list = []
    for patient in patients:
        if not patient.date_of_birth:
            continue
        try:
            age = calculate_age(patient.date_of_birth)
            age_list.append(age)
        except ValueError:
            continue
    if not age_list:
        return jsonify({'message': 'No valid dates of birth found for patients.'}), 400
    age_df = pd.DataFrame(age_list, columns=['age'])
    age_counts = age_df['age'].value_counts().sort_index()

    # Create bar chart
    fig, ax = plt.subplots()
    ax.bar(age_counts.index, age_counts.values)
    ax.set_xlabel('Age')
    ax.set_ylabel('Number of patients')
    ax.set_title('Age distribution of patients')

    # Convert chart to base64 encoded PNG image

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    chart = base64.b64encode(buf.read()).decode('utf-8')

    result = {
        'age_analysis': chart,
        'medication_frequency': get_medication_frequency(),
        'get_medication_dosages': get_medication_dosages(),

    }
    return render_template('age_analysis.html', result=result)


def get_medication_frequency():
    medication_frequency = aggregate_medications_by_frequency()
    medication_frequency_dict = dict(medication_frequency)
    frequencies = list(medication_frequency_dict.keys())
    counts = list(medication_frequency_dict.values())

    # Create your plot
    fig, ax = plt.subplots()
    x = np.arange(len(frequencies))
    ax.bar(x, counts)
    ax.set_xticks(x)
    ax.set_xticklabels(frequencies)
    ax.set_ylabel('Count')
    ax.set_title('Medication Frequency')

    # Save your plot to a file
    fig.savefig('medication_frequency.png')
    # Convert chart to base64 encoded PNG image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    chart = base64.b64encode(buf.read()).decode('utf-8')
    # Return your plot file as a JSON response
    result = {
        'chart': chart
    }
    return result['chart']


def get_medication_dosages():
    dosage_totals = aggregate_medication_dosages()
    total_dosages = list(dosage_totals.values())

    # Create your plot
    fig, ax = plt.subplots()
    ax.hist(total_dosages, bins=10)
    ax.set_xlabel('Total Dosage')
    ax.set_ylabel('Frequency')
    ax.set_title('Medication Dosages')

    # Save your plot to a file
    fig.savefig('medication_dosages.png')
    # Convert chart to base64 encoded PNG image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    chart = base64.b64encode(buf.read()).decode('utf-8')
    # Return your plot file as a JSON response
    result = {
        'dosage_totals': dosage_totals,
        'chart': chart
    }
    return result['chart']


@analysis_bp.route('/medication-dosage', methods=['GET'])
def get_medication_dosage():
    medication_dosages = aggregate_medication_dosages()
    medication_dosages_dict = dict(medication_dosages)

    # Create plot
    fig, ax = plt.subplots()
    ax.pie(medication_dosages_dict.values(), labels=medication_dosages_dict.keys(), autopct='%1.1f%%')
    ax.set_title('Medication Dosages For each Patient')

    # Save your plot to a file
    fig.savefig('medication_dosage.png')

    # Convert chart to base64 encoded PNG image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    chart = base64.b64encode(buf.read()).decode('utf-8')

    # Return your plot file as a JSON response
    result = {
        'medication_dosages': medication_dosages,
        'chart': chart
    }
    return render_template('dosage_analysis.html', result=result)
