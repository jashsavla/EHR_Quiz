#!/bin/bash

# Navigate to the backend folder
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
  # Windows
  venv\Scripts\activate
else
  # macOS/Linux
  source venv/bin/activate
fi

# Install required packages
pip install flask flask-sqlalchemy psycopg2-binary flask-cors

# Run the Flask app
python app.py