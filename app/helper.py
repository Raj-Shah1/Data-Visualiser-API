def format_column_headers(column_headers):
    formatted_headers = []
    for header in column_headers:
        formatted_header = " ".join(word.capitalize() for word in header.split("_"))
        formatted_headers.append(formatted_header)
    return formatted_headers
