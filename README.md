Flask Project README
This project is a Flask web application about patient and medications.

Installation
To run this project, you will need to have Python 3 installed on your machine.

Clone the repository onto your local machine.
Create a virtual environment: python3 -m venv venv or by: virtualenv --python="specify your python location" venv
Activate the virtual environment:
On Windows: venv\Scripts\activate.bat
On Unix or Linux: source venv/bin/activate
Install the project dependencies: pip install -r requirements.txt
Set the Flask app environment variable:
On Windows: set FLASK_APP=app.py
On Unix or Linux: export FLASK_APP=app.py
Create the database: flask db create
Run the migrations: flask db upgrade
Usage
To run the Flask app, execute flask run. By default, the app will be available at http://localhost:5000/.

Migrations
If you need to make changes to the database schema, you will need to create a migration. Here are the steps to create and apply a migration:

Make changes to your database models.
Generate a migration: flask db migrate -m "Description of migration"
Review the generated migration script in the migrations/versions directory.
Apply the migration: flask db upgrade
If you need to undo a migration, you can use the flask db downgrade command.
