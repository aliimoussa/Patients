


# Use an official Python runtime as a parent image
FROM python:3.9

WORKDIR /app

# Install application dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy application code
COPY myproject /app/myproject
COPY app.py /app/app.py

# Set environment variables
ENV FLASK_APP=app.py



# Expose the default Flask port
EXPOSE 5000

# Start the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
