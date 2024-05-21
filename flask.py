from flask import Flask
import psycopg2, jsonify

app = Flask(__name__)


DATABASE_HOST = "postgres"
DATABASE_PORT = 5432
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "123456"
DATABASE_NAME = "postgres"

def connect_to_db():
  """Connects to the PostgreSQL database and returns a connection object."""
  connection = None
  try:
    connection = psycopg2.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )
  except Exception as error:
    print("Error connecting to PostgreSQL database:", error)
  return connection


@app.route("/provinces")
def get_data():
  """Executes a SELECT query and returns the results as JSON."""
  connection = connect_to_db()
  if connection is None:
    return jsonify({"error": "Failed to connect to database"}), 500

  cursor = connection.cursor()
  try:
    # Replace 'your_query' with your actual SELECT query
    cursor.execute("SELECT * FROM provinces")
    rows = cursor.fetchall()
    return rows
  except Exception as error:
    print("Error fetching data from database:", error)
    return jsonify({"error": "Failed to retrieve data"}), 500
  finally:
    if connection:
      connection.close()

@app.route("/cities")
def get_cities():
  """Executes a SELECT query and returns the results as JSON."""
  connection = connect_to_db()
  if connection is None:
    return jsonify({"error": "Failed to connect to database"}), 500

  cursor = connection.cursor()
  try:
    # Replace 'your_query' with your actual SELECT query
    cursor.execute(f"""select 
                cities.id,
                cities.name as city_name,
                provinces.name as province_name,
                provinces.population 
            from cities 
            join provinces 
                on cities.province_id = provinces.id""")
    rows = cursor.fetchall()
    return rows
  except Exception as error:
    print("Error fetching data from database:", error)
    return jsonify({"error": "Failed to retrieve data"}), 500
  finally:
    if connection:
      connection.close()

@app.route("/provinces/<province_id>")
def get_data_by_param(province_id):
  connection = connect_to_db()
  if connection is None:
    return jsonify({"error": "Failed to connect to database"}), 500

  cursor = connection.cursor()
  try:
    query = f"SELECT cities.name as city_name, provinces.name as province_name FROM cities left join provinces on provinces.id = cities.province_id WHERE province_id = %s"
    cursor.execute(query, (province_id, ))
    rows = cursor.fetchall()
    return rows
  except Exception as error:
    print("Error fetching data from database:", error)
    return jsonify({"error": "Failed to retrieve data"}), 500
  finally:
    if connection:
      connection.close()


@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route('/1')
def hello_world1():
    return 'Hello, another route!'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)