from flask import Flask, request, jsonify
import vanna
from vanna.remote import VannaDefault

app = Flask(__name__)

api_key = "d5ed6960a5cc42e59e452d4bd083dec8"
vanna_model_name = "custommodeltest"
vn = VannaDefault(model=vanna_model_name, api_key=api_key)
vn.connect_to_duckdb(url=':memory:')

# Load the dataset into the DuckDB in-memory database
vn.run_sql("""CREATE TABLE Table4 AS SELECT * FROM 'E:\SqlRoute\DataTest.csv';""")

# Route to get information schema
@app.route('/information_schema', methods=['GET'])
def get_information_schema():
    df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
    return df_information_schema.to_json()

# Route to train the model with the schema
@app.route('/train_schema', methods=['POST'])
def train_schema():
    df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
    plan = vn.get_training_plan_generic(df_information_schema)
    vn.train(plan=plan)
    return jsonify({"status": "Schema training complete"})

# Route to train the model with specific DDL
@app.route('/train_ddl', methods=['POST'])
def train_ddl():
    vn.train(ddl="DESCRIBE SELECT * FROM Table4")
    return jsonify({"status": "DDL training complete"})

# Route to train the model with SQL statements
@app.route('/train_sql', methods=['POST'])
def train_sql():
    question = request.json.get("question")
    sql = request.json.get("sql")
    vn.train(question=question, sql=sql)
    return jsonify({"status": "SQL training complete"})

# Route to provide documentation context
@app.route('/train_documentation', methods=['POST'])
def train_documentation():
    documentation = request.json.get("documentation")
    vn.train(documentation=documentation)
    return jsonify({"status": "Documentation training complete"})

# Route to ask a question
@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.json.get("question")
    response = vn.ask(question, visualize=False)
    return jsonify({"response": response})

# Route to generate SQL
@app.route('/generate_sql', methods=['POST'])
def generate_sql():
    question = request.json.get("question")
    sql = vn.generate_sql(question)
    return jsonify({"sql": sql})

if __name__ == '__main__':
    app.run(debug=True)
