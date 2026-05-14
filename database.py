import hashlib
import sqlite3
import subprocess
import pickle

DB_PASSWORD = "super_secret_123"
DB_NAME = "production_db"

# Bu fonksiyon kullanici girdisi aliyor - gercek acik
def get_user(user_id):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = " + user_id)
    return cur.fetchone()

# MD5 - guvenlik icin kullaniliyor - gercek acik
def hash_password(data):
    return hashlib.md5(data.encode()).hexdigest()

# Shell=True - kullanici girdisi gecebilir - gercek acik
def run_report(filename):
    result = subprocess.check_output("cat " + filename, shell=True)
    return result.decode()

# Pickle - uzaktan kod calistirma riski
def load_user_session(session_data):
    return pickle.loads(session_data)

# Test icin mock - false positive olmali
def _test_hash():
    return hashlib.md5(b"test").hexdigest()
