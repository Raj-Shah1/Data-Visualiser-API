import psycopg2
from dotenv import load_dotenv

load_dotenv()

import os

db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


def connect_to_database():
    try:
        connection = psycopg2.connect(**db_config)
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


# def connect_to_database():
#     # Step 1: Import the necessary modules

#     # Step 2: Create a SQLAlchemy Engine
#     # Replace 'postgresql://username:password@hostname:port/database_name' with your PostgreSQL connection URL
#     # For example, if you have a local PostgreSQL server with username 'myuser' and no password on the 'mydatabase' database:
#     # engine = create_engine('postgresql://myuser:@localhost:5432/mydatabase')
#     engine = create_engine(os.getenv("DATABASE_CONNECTION_URL"))

#     # Step 3: Establish a connection to the PostgreSQL database
#     connection = engine.connect()

#     # Step 4: Perform database operations
#     # For example, you can execute SQL queries using the connection:
#     # result = connection.execute("SELECT * FROM rental LIMIT 10")
#     # for row in result:
#     #     print(row)

#     return connection
