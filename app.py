"""
Vulnerable demo app for SAST analysis with Bandit.
DO NOT use this code in production - it is intentionally insecure.
"""
import hashlib
import pickle
import random
import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)

# Issue 1: hardcoded credentials
DB_PASSWORD = "SuperSecret123!"


@app.route("/user")
def get_user():
    # Issue 2: SQL injection (string concatenation)
    username = request.args.get("username")
    conn = sqlite3.connect("users.db")
    query = "SELECT * FROM users WHERE name = '%s'" % username
    return str(conn.execute(query).fetchall())


@app.route("/ping")
def ping():
    # Issue 3: command injection (shell=True with user input)
    host = request.args.get("host")
    result = subprocess.check_output("ping -c 1 " + host, shell=True)
    return result


@app.route("/login", methods=["POST"])
def login():
    # Issue 4: weak hashing algorithm (MD5)
    password = request.form.get("password", "")
    return hashlib.md5(password.encode()).hexdigest()


@app.route("/token")
def token():
    # Issue 5: insecure randomness for security tokens
    return str(random.randint(100000, 999999))


@app.route("/load", methods=["POST"])
def load():
    # Issue 6: insecure deserialization
    return str(pickle.loads(request.data))


if __name__ == "__main__":
    # Issue 7: debug mode enabled in production
    app.run(host="0.0.0.0", debug=True)
