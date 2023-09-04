import psycopg2
from app import app

from sqlalchemy import create_engine, MetaData, Table, inspect, text
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


def get_create_table_queries():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                'CREATE TABLE ' || table_name || ' (' || STRING_AGG(column_definition, ', ') || ');'
            FROM (
                SELECT
                    table_name,
                    column_name || ' ' || data_type ||
                    CASE
                        WHEN character_maximum_length IS NOT NULL THEN '(' || character_maximum_length || ')'
                        ELSE ''
                    END AS column_definition
                FROM information_schema.columns
                WHERE table_schema = 'public'
            ) AS table_columns
            GROUP BY table_name;
        """
        )
        create_table_queries = cursor.fetchall()
        connection.close()
        return create_table_queries
    else:
        return []


# def get_create_table_queries():
#     try:
#         # Step 2: Create a SQLAlchemy Engine
#         engine = create_engine(os.getenv("DATABASE_CONNECTION_URL"))

#         # Step 3: Create a MetaData object without a bind
#         metadata = MetaData()
#         reflect = metadata.reflect(bind=engine)

#         create_table_queries = []

#         # Step 4: Use the inspect module to get table names
#         inspector = inspect(engine)
#         table_names = inspector.get_table_names()

#         # Step 5: Reflect individual tables with a specific bind and retrieve CREATE TABLE queries
#         for table_name in table_names:
#             table = Table(table_name, metadata, autoload_with=engine)
#             create_table_query = text(table.schema())
#             create_table_queries.append(str(create_table_query))

#         return create_table_queries
#     except Exception as e:
#         print(f"Error getting CREATE TABLE queries: {e}")
#         return []


def execute_query(query):
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()

        try:
            cursor.execute(query)
        except Exception as e:
            print(f"Error executing query: {e}")
            return [], []

        # Get the column headers
        column_headers = [desc[0] for desc in cursor.description]

        # Fetch all rows
        result = cursor.fetchall()
        connection.close()

        # Return column headers and query result
        return column_headers, result
    else:
        return [], []
