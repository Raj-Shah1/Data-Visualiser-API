import openai

from app.db import get_create_table_queries
from dotenv import load_dotenv

load_dotenv()

import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def openai_query_generation(question):
    create_table_queries = get_create_table_queries()
    create_tables_sql = ""
    if create_table_queries:
        create_tables_sql = "\n\n".join([row[0] for row in create_table_queries])
    else:
        return "<p>Error retrieving CREATE TABLE statements.</p>"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Given the following SQL tables, your job is to write queries given a user’s request. The database is postgresql and output should only contain query and nothing else\n\n"
                + create_tables_sql,
            },
            {
                "role": "user",
                "content": question,
                # "content": "Write a SQL query which computes the average total order value for all orders on 2023-04-01.",
            },
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Process the response as needed
    # For example, you can extract the response and return it
    answer = response["choices"][0]["message"]["content"]
    return answer
