from flask import Flask, request, make_response
import mysql.connector
import datetime

app = Flask(__name)

# Database configuration
db = mysql.connector.connect(
    host="db",
    user="root",
    password="password",
    database="mydb"
)

# Counter
counter = 0

@app.route("/")
def home():
    global counter
    counter += 1
    cur = db.cursor()
    cur.execute("INSERT INTO access_log (access_time, client_ip, server_ip) VALUES (%s, %s, %s)",
                (datetime.datetime.now(), request.remote_addr, request.environ['REMOTE_ADDR']))
    db.commit()

    response = make_response("Internal IP address of the server: " + request.environ['REMOTE_ADDR'])
    response.set_cookie('internal_ip', request.environ['REMOTE_ADDR'], max_age=300)
    return response

@app.route("/showcount")
def show_count():
    global counter
    return f"Global counter number: {counter}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
