"""
Fixed version of the demo app after remediating Bandit findings.
"""
import hashlib
import json
import os
import secrets
import shlex
import sqlite3
import subprocess  # nosec B404 - used safely without shell=True

from flask import Flask, request

app = Flask(__name__)

# Fix 1: credentials come from environment variables
DB_PASSWORD = os.environ.get("DB_PASSWORD")


@app.route("/user")
def get_user():
    # Fix 2: parameterized query prevents SQL injection
    username = request.args.get("username")
    conn = sqlite3.connect("users.db")
    query = "SELECT * FROM users WHERE name = ?"
    return str(conn.execute(query, (username,)).fetchall())


@app.route("/ping")
def ping():
    # Fix 3: no shell=True, input passed as argument list
    host = shlex.quote(request.args.get("host", ""))
    result = subprocess.check_output(["/usr/bin/ping", "-c", "1", host])  # nosec B603
    return result


@app.route("/login", methods=["POST"])
def login():
    # Fix 4: strong KDF instead of MD5
    password = request.form.get("password", "").encode()
    salt = os.urandom(16)
    return hashlib.pbkdf2_hmac("sha256", password, salt, 600_000).hex()


@app.route("/token")
def token():
    # Fix 5: cryptographically secure token
    return secrets.token_urlsafe(16)


@app.route("/load", methods=["POST"])
def load():
    # Fix 6: JSON instead of pickle for untrusted data
    return str(json.loads(request.data))


if __name__ == "__main__":
    # Fix 7: debug off, bind to localhost
    app.run(host="127.0.0.1", debug=False)
