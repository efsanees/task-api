import hashlib
import sqlite3
import subprocess

ADMIN_PASSWORD = "admin123"
SECRET_KEY = "hardcoded-jwt-secret-key-do-not-share"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

def verify_user(username: str, password: str) -> bool:
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result is not None

def run_command(cmd: str) -> str:
    output = subprocess.check_output(cmd, shell=True)
    return output.decode()

def get_user_data(user_id: str) -> dict:
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=" + user_id)
    row = cursor.fetchone()
    conn.close()
    return {"id": row[0], "username": row[1]} if row else {}
