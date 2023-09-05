from flask import Response, request, jsonify
from app import app
from app.openai_api import openai_query_generation
from app.db import create_sql_queries_table, create_sql_queries_record, get_sql_queries_by_name
from app.db import get_sql_queries, update_sql_query_record, delete_sql_query_record
from app.service.fetch_graph_data import table_data
import json


@app.route("/generate-query", methods=["POST"])
def generate_query_route():

    json_data = request.json
    if json_data is None:
        return jsonify({"error": "Invalid JSON data"}), 400

    question = str(json_data['question'])
    if question:
        answer = openai_query_generation(question)
        return Response(answer, mimetype="text/plain")
    else:
        return "Please provide a user question in the 'question' parameter.", 400  


@app.route("/execute-query", methods=["POST"])
def execute_query_route():
    
    json_data = request.json
    if json_data is None:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    query = str(json_data['query'])

    google_table_data = table_data(query)

    if google_table_data:
        # Convert the data to JSON and encode it as bytes
        json_data_bytes = json.dumps(google_table_data).encode('utf-8')
        return Response(json_data_bytes, mimetype="application/json")
    else:
        return "Please provide a user query in the 'user_query' parameter.", 400


@app.route("/save-query", methods=["POST"])
def save_query_route():
    json_data = request.json
    if json_data is None:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    query = str(json_data['query'])
    query_name = str(json_data['query_name'])

    create_sql_queries_table()
    sql_query_data = get_sql_queries_by_name(query_name)

    if not sql_query_data:  # Check if the query does not already exist
        create_sql_queries_record(query_name, query)
        return "Query saved successfully.", 200
    else:
        return "Record already exists. Kindly update the query name", 400
    

@app.route("/get-query", methods=["GET"])
def get_query_route():
    query_result = get_sql_queries()
    # Convert the data to JSON and encode it as bytes
    json_data_bytes = json.dumps(query_result).encode('utf-8')
    return Response(json_data_bytes, mimetype="application/json")


@app.route("/update-query", methods=["POST"])
def update_query_route():
    json_data = request.json
    if json_data is None:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    query = str(json_data['query'])
    query_name = str(json_data['query_name'])

    sql_query_data = get_sql_queries_by_name(query_name)

    if sql_query_data:  # Check if the query does not already exist
        update_sql_query_record(query_name, query)
        return "Query saved successfully.", 200
    else:
        return "Record already exists. Kindly update the query name", 400
    

@app.route("/delete-query", methods=["POST"])
def delete_query_route():
    json_data = request.json
    if json_data is None:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    query_name = str(json_data['query_name'])

    delete_sql_query_record(query_name)

    return "Query deleted successfully.", 200