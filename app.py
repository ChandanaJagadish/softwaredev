from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# --- Initialize DB ---
def init_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, age INTEGER, course TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_student():
    data = request.json
    name, age, course = data["name"], data["age"], data["course"]

    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", (name, age, course))
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

@app.route("/list", methods=["GET"])
def list_students():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = [{"id": row[0], "name": row[1], "age": row[2], "course": row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify(students)

if __name__ == "__main__":
    app.run(debug=True)
