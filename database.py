import hashlib
import sqlite3
import subprocess
import pickle

DB_PASSWORD = "super_secret_123"
DB_NAME = "production_db"

def get_user(user_id):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = " + user_id)
    return cur.fetchone()

def hash_data(data):
    return hashlib.md5(data.encode()).hexdigest()

def run_report(filename):
    result = subprocess.check_output("cat " + filename, shell=True)
    return result.decode()

def load_user_session(session_data):
    return pickle.loads(session_data)
