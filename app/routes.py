from decimal import Decimal
from flask import Response, request, jsonify
from app import app
from app.openai_api import openai_query_generation
from app.db import execute_query, create_sql_queries_table, create_sql_queries_record, get_sql_queries_by_name
from app.helper import format_column_headers
from app.service.fetch_graph_data import table_data


@app.route("/generate-query", methods=["POST"])
def generate_query_route():

    json_data = request.json
    if json_data is None:
        return jsonify({"error": "Invalid JSON data"}), 400

    user_question = str(json_data['user_question'])
    if user_question:
        answer = openai_query_generation(user_question)
        return Response(answer, mimetype="text/plain")
    else:
        return "Please provide a user question in the 'user_question' parameter.", 400  


@app.route("/execute-query", methods=["POST"])
def execute_query_route():
    user_query = request.form.get("user_query")

    google_table_data = table_data(user_query)

    if google_table_data:
        return Response(google_table_data, mimetype="text/plain")
    else:
        return "Please provide a user query in the 'user_query' parameter.", 400
