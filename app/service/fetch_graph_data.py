from decimal import Decimal
from app.db import execute_query
from app.helper import format_column_headers


def table_data(query):
    data = []
    if query:
        column_headers, answer = execute_query(query)

        formatted_column_headers = format_column_headers(column_headers)

        # Ensure that 'answer' is a list of lists containing table data
        if not isinstance(answer, list) or not all(
            isinstance(row, list) for row in answer
        ):
            data = [list(t) for t in answer]

        for row in data:
            for i in range(len(row)):
                if isinstance(row[i], Decimal):
                    row[i] = float(row[i])

        # Convert the data into a format suitable for Google Table Chart
        google_table_data = [formatted_column_headers] + data
        return google_table_data
