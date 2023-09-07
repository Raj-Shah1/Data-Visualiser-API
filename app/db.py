import psycopg2
from app import app
from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, inspect, text
from dotenv import load_dotenv
from run import connection

load_dotenv()

def get_create_table_queries():
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

        # Return column headers and query result
        return column_headers, result
    else:
        return [], []
  

def create_sql_queries_table():
    if connection:
        cursor = connection.cursor()
        try:
            # Create the 'sql_queries' table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sql_queries (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200) UNIQUE NOT NULL,
                    query TEXT,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                );
            """)
            connection.commit()
            print("'sql_queries' table created successfully.")
        except Exception as e:
            print(f"Error creating 'sql_queries' table: {e}")
            connection.rollback()


def create_sql_queries_record(name, query):
    
    print("query_name: ", name)
    print("query: ", query)
    if connection:
        cursor = connection.cursor()
        try:
            # Insert a new record into the 'sql_queries' table
            cursor.execute("""
                INSERT INTO sql_queries (name, query)
                VALUES (%s, %s);
            """, (name, query))
            connection.commit()
            print("SQL query record created successfully.")
        except Exception as e:
            print(f"Error creating SQL query record: {e}")
            connection.rollback()


def get_sql_queries_by_name(name):
    if connection:
        cursor = connection.cursor()
        try:
            # Retrieve the SQL query record by name
            cursor.execute("""
                SELECT id FROM sql_queries
                WHERE name = %s;
            """, (name,))
            query_result = cursor.fetchone()
            if query_result:
                query = query_result[0]
                print(f"SQL query with name '{name}' found.")
                return query
            else:
                print(f"No SQL query found with name '{name}'.")
                return None
        except Exception as e:
            return (f"Error retrieving SQL query by name: {e}")
    else:
        return None
    

def get_sql_queries_by_id(id):
    if connection:
        cursor = connection.cursor()
        try:
            # Retrieve the SQL query record by name
            cursor.execute("""
                SELECT id FROM sql_queries
                WHERE id = %s;
            """, (id,))
            query_result = cursor.fetchone()
            if query_result:
                query = query_result[0]
                print(f"SQL query with id '{id}' found.")
                return query
            else:
                print(f"No SQL query found with id '{id}'.")
                return None
        except Exception as e:
            return (f"Error retrieving SQL query by id: {e}")
    else:
        return None
    

def get_sql_queries():
    if connection:
        cursor = connection.cursor()
        try:
            # Retrieve the SQL query records
            cursor.execute("""
                SELECT id, name, query FROM sql_queries 
                ORDER BY updated_at DESC;
            """)
            query_result = cursor.fetchall()
            return [{"id": id, "name": name, "query": query} for id, name, query in query_result]
        except Exception as e:
            return (f"Error retrieving SQL query records: {e}")
    else:
        return None
    

def update_sql_query_record(id, query):
    if connection:
        cursor = connection.cursor()
        try:
            # Update the SQL query record
            cursor.execute("""
                UPDATE sql_queries
                SET query = %s, updated_at = %s
                WHERE id = %s;
            """, (query, datetime.now(), id))
            connection.commit()
            print("SQL query record updated successfully.")
        except Exception as e:
            print(f"Error updating SQL query record: {e}")
            connection.rollback()


def delete_sql_query_record(id):
    if connection:
        cursor = connection.cursor()
        try:
            # Delete the SQL query record
            cursor.execute("""
                DELETE FROM sql_queries
                WHERE id = %s;
            """, (id,))
            connection.commit()
            print("SQL query record deleted successfully.")
        except Exception as e:
            print(f"Error deleting SQL query record: {e}")
            connection.rollback()
    