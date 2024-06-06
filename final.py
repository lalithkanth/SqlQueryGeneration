from flask import Flask, request, jsonify
import vanna
from vanna.remote import VannaDefault

app = Flask(__name__)

# API key and model configuration
api_key = "d5ed6960a5cc42e59e452d4bd083dec8"
vanna_model_name = "custommodeltest"
vn = VannaDefault(model=vanna_model_name, api_key=api_key)

# Connect to an in-memory DuckDB instance
vn.connect_to_duckdb(url=':memory:')

# Create the initial table (empty table for demonstration)
vn.run_sql("""CREATE TABLE Table7 AS SELECT * FROM 'E:\SqlRoute\DataTest.csv';SELECT * FROM Table7""")

@app.route('/generate_sql', methods=['POST'])
def generate_sql():
    # Retrieve question from request
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "Question is required"}), 400

    # Generate SQL query
    try:
        sql_query = vn.generate_sql(question)
        return jsonify({"sql_query": sql_query})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
