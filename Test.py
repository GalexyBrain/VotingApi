from flask import Flask, request, jsonify
import shelve
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
loggedIn = False

@app.route('/')
def index():
    return "hello world"

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        epicId = request.form.get('epicid')
        solidityNumber = request.form.get('solidityid')
        
        if not epicId or not solidityNumber:
            return jsonify({"message": "epicid and solidityid are required"}), 400
        
        try:
            with shelve.open("Test.db") as db:
                if epicId in db and db[epicId] == solidityNumber:
                    return parseBlockChain(epicId)
                elif epicId not in db:
                    return jsonify({"message": "User not found"}), 404
                else:
                    return jsonify({"message": "Wrong password"}), 401
        except Exception as e:
            return jsonify({"message": str(e)}), 405
    
def parseBlockChain(epicId):
    global loggedIn
    #parse the block chain
    
    loggedIn = True
    return jsonify({"message": "Login Successful"}), 200

@app.route('/vote', methods=["POST"])
def vote():
    if loggedIn == False:
        return jsonify({"message": "Ayy hackor"}), 401
    if request.method == "POST":
        try:
            # Establish a connection to the MySQL server
            connection = mysql.connector.connect(
                host='localhost',
                user='Thejus',
                password='root',
                database='vote'
            )

            if connection.is_connected():
                print("Connected to MySQL server")
            epicId = request.form['id']
            party = request.form['party']
            
            cursor = connection.cursor()
            cursor.execute("update party set votes = votes + 1 where name = '{}'".format(party))
            
            #raise event for block chain

            connection.commit()
                
        except Error as e:
            return jsonify({"message" : "Error while connecting to MySQL" + e}), 400
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
        
    return jsonify({"message": "Vote Successful"}), 200

if __name__ == '__main__':
    app.run(debug=True)
