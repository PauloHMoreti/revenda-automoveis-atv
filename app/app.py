import os

from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

@app.route("/")
def home():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "host.docker.internal"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "meubanco")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT 'Hello from MySQL!'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("index.html", msg=result[0])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
