from flask import Response, request, jsonify
from app import app
from app.openai_api import openai_query_generation
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
