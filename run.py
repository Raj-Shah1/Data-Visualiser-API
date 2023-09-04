from flask import Flask
from flask_cors import CORS
from app import app
from app.db import connect_to_database

# Enable CORS for all routes
CORS(app)

if __name__ == "__main__":
    # Connect to the database
    connection = connect_to_database()
    if not connection:
        raise Exception("Error connecting to the database")

    # Run the Flask app
    app.run(host='127.0.0.1', port=5000)
