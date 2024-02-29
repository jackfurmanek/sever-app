from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
from datetime import datetime

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Your existing routes
@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route("/pokemon")
def pokemon():
    return {"pokemon": ["Bulbasaur", "Charmander", "Squirtle"]}

# New route for adding a quit entry
@app.route("/add_quit", methods=['POST'])
def add_quit():
    data = request.json  # Assuming the input data is JSON
    name = data['name']
    rate = data['rate']
    time_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S+00')  # Current time in UTC
    
    try:
        conn = psycopg2.connect(database="sever_db",
                                host="localhost",
                                user="postgres",
                                password="password",
                                port="5432")
        cur = conn.cursor()
        
        cur.execute("""INSERT INTO quits (name, time_added, rate) VALUES (%s, %s, %s);""",
                    (name, time_added, rate))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Quit entry added successfully", "name": name, "rate": rate, "time_added": time_added})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route("/get_quits", methods=['GET'])
def get_quits():
    try:
        conn = psycopg2.connect(database="sever_db",
                                host="localhost",
                                user="postgres",
                                password="password",
                                port="5432")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("SELECT * FROM quits;")
        quits = cur.fetchall()
        
        # Convert list of psycopg2 DictRow objects to list of dicts
        quits_list = [dict(quit) for quit in quits]
        
        cur.close()
        conn.close()
        
        return jsonify(quits_list)
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/delete_quit/<int:quit_id>', methods=['DELETE'])
def delete_quit(quit_id):
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(database="sever_db", user="postgres", password="password", host="localhost", port="5432")
        cur = conn.cursor()
        
        # Execute the DELETE statement
        cur.execute("DELETE FROM quits WHERE id = %s", (quit_id,))
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
        # Return a success message
        return jsonify({"message": "Quit entry deleted successfully"}), 200
    except Exception as e:
        # In case of any exception, return an error message
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
