from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'database.db'

# Criação automática da tabela
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                start_time TEXT NOT NULL,
                end_time TEXT,
                FOREIGN KEY(task_id) REFERENCES tasks(id)
            )
        ''')

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form['task']
    created_at = datetime.now().isoformat()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (name, created_at) VALUES (?, ?)', (task_name, created_at))
    return redirect(url_for('index'))

@app.route('/start/<int:task_id>')
def start_session(task_id):
    start_time = datetime.now().isoformat()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sessions (task_id, start_time) VALUES (?, ?)', (task_id, start_time))
    return redirect(url_for('index'))

@app.route('/history')
def history():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.id, t.name, s.start_time, s.end_time
            FROM sessions s
            JOIN tasks t ON s.task_id = t.id
            ORDER BY s.start_time DESC
        ''')
        sessions = cursor.fetchall()
    return render_template('history.html', sessions=sessions)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
