from flask import Flask, request, jsonify
from vanna.remote import VannaDefault

app = Flask(__name__)

api_key = "d5ed6960a5cc42e59e452d4bd083dec8"
vanna_model_name = "custommodeltest"
vn = VannaDefault(model=vanna_model_name, api_key=api_key)
vn.connect_to_duckdb(url=':memory:')

@app.route('/generate_sql', methods=['POST'])
def generate_sql():
    data = request.get_json()

    if 'question' in data:
        question = data['question']
        sql_query = vn.generate_sql(question)
        return jsonify({'sql_query': sql_query})
    else:
        return jsonify({'error': 'Question parameter not found'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
