from flask import Flask
from app import app
from app.db import connect_to_database

if __name__ == "__main__":
    # Connect to the database
    connection = connect_to_database()
    if not connection:
        raise Exception("Error connecting to the database")

    # Run the Flask app
    app.run()
