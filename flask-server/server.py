from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask_sqlalchemy import SQLAlchemy
import threading

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

lock = threading.Lock()

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/sever_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Quit model corresponding to the 'quits_t' table in the database
class Quit(db.Model):
    __tablename__ = 'quits_t'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rate = db.Column(db.Float, index=True)
    time_added = db.Column(db.DateTime)
    type_id = db.Column(db.Integer, db.ForeignKey('types_t.id'))  # ForeignKey pointing to the Type table

    # 'type' is the backref that will be added to the Type model
    # It allows you to access the type of a quit directly by quit.type thanks to the backref
    # No need to define a relationship on the Type class as it's done implicitly through the ForeignKey and backref

    def __repr__(self):
        return f'<Quit {self.name}>'

class Type(db.Model):
    __tablename__ = 'types_t'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    
    # The 'quits' relationship allows you to access all quits of a type by type.quits
    # The 'backref' defines a property on the Quit instances to access their Type
    quits = db.relationship('Quit', backref='type', lazy=True)

    def __repr__(self):
        return f'<Type {self.name}>'

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
    lock.acquire()
    try:

        data = request.json  # Assuming the input data is JSON
        print(data)
        name = data['name']
        rate = data['rate']
        time_added = data['time_added']
        type_id = data.get('type_id')  # Extract type_id from the request JSON
        
        # Ensure type_id is not None or convert it to a default value, depending on your database schema requirements
        if type_id is None:
            return jsonify({"error": "type_id is required"}), 400  # Or set a default value if appropriate

        try:
            conn = psycopg2.connect(database="sever_db",
                                    host="localhost",
                                    user="postgres",
                                    password="password",
                                    port="5432")
            cur = conn.cursor()
            
            # Include type_id in the INSERT statement
            cur.execute("""INSERT INTO quits_t (name, time_added, rate, type_id) VALUES (%s, %s, %s, %s);""",
                        (name, time_added, rate, type_id))
            
            conn.commit()
            cur.close()
            conn.close()
            
            return jsonify({"message": "Quit entry added successfully", "name": name, "rate": rate, "time_added": time_added, "type_id": type_id})
        except Exception as e:
            return jsonify({"error": str(e)})
    finally:
        lock.release()
    
@app.route("/get_quits", methods=['GET'])
def get_quits():
    try:
        conn = psycopg2.connect(database="sever_db",
                                host="localhost",
                                user="postgres",
                                password="password",
                                port="5432")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("""SELECT quits_t.name AS name, quits_t.rate, types_t.name AS type_name, quits_t.id
                    FROM quits_t
                        JOIN types_t
                            ON quits_t.type_id = types_t.id;""")
        quits = cur.fetchall()
        
        # Convert list of psycopg2 DictRow objects to list of dicts
        quits_list = [dict(quit) for quit in quits]
        
        cur.close()
        conn.close()
        
        return jsonify(quits_list)
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route("/get_types", methods=['GET'])
def get_types():
    try:
        conn = psycopg2.connect(database="sever_db",
                                host="localhost",
                                user="postgres",
                                password="password",
                                port="5432")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("SELECT * FROM types_t;")
        quits = cur.fetchall()
        
        # Convert list of psycopg2 DictRow objects to list of dicts
        quits_list = [dict(quit) for quit in quits]
        
        cur.close()
        conn.close()
        
        return jsonify(quits_list)
    except Exception as e:
        return jsonify({"error": str(e)})
    
# @app.route('/delete_quit/<int:quit_id>', methods=['DELETE'])
# def delete_quit(quit_id):
#     try:
#         # Establish a connection to the database
#         conn = psycopg2.connect(database="sever_db", user="postgres", password="password", host="localhost", port="5432")
#         cur = conn.cursor()
        
#         # Execute the DELETE statement
#         cur.execute("DELETE FROM quits_t WHERE id = %s", (quit_id,))
        
#         # Commit the transaction
#         conn.commit()
        
#         # Close the cursor and connection
#         cur.close()
#         conn.close()
        
#         # Return a success message
#         return jsonify({"message": "Quit entry deleted successfully"}), 200
#     except Exception as e:
#         # In case of any exception, return an error message
#         return jsonify({"error": str(e)}), 500

@app.route('/delete_quit/<int:quit_id>', methods=['DELETE'])
def delete_quit(quit_id):
    try:
        quit = Quit.query.get(quit_id)
        if quit is None:
            return jsonify({"error": "Quit entry not found"}), 404

        db.session.delete(quit)
        db.session.commit()
        return jsonify({"message": "Quit entry deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
def calculate_months_since(date_string):
    date_added = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S+00') # Adjust format if necessary
    now = datetime.now()
    delta = relativedelta(now, date_added)
    return delta.years * 12 + delta.months

@app.route('/update_quit/<int:quit_id>', methods=['PUT', 'PATCH'])
def update_quit(quit_id):
    data = request.json
    try:
        conn = psycopg2.connect(database="sever_db", user="postgres", password="password", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute("UPDATE quits_t SET name = %s, rate = %s WHERE id = %s",
                    (data['name'], data['rate'], quit_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Quit entry updated successfully"}), 200
    except Exception as e:
        # In case of any exception, return an error message
        return jsonify({"error": str(e)}), 500
    

@app.route('/highest_valued_quit/<int:type_id>', methods=['GET'])
def highest_valued_quit(type_id):
    try:
        # Using SQLAlchemy to perform a join and find the highest rate quit for the specified type
        quit = db.session.query(Quit).join(Type, Quit.type_id == Type.id)\
            .filter(Type.id == type_id)\
            .order_by(Quit.rate.desc())\
            .first()
        if quit:
            return jsonify({
                "id": quit.id,
                "name": quit.name,
                "rate": quit.rate,
                "type_name": quit.type.name,
                "time_added": quit.time_added.strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return jsonify({"error": "No quits found for the specified type"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)