from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
DB_NAME = 'database.db'

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
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
    if not task:
        abort(404)
    return render_template('pomodoro.html', task_id=task[0], task_name=task[1])

@app.route('/end/<int:session_id>')
def end_session(session_id):
    end_time = datetime.now().isoformat()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE sessions SET end_time = ? WHERE id = ?', (end_time, session_id))
    return redirect(url_for('history'))

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

        cursor.execute('SELECT start_time, end_time FROM sessions WHERE end_time IS NOT NULL')
        all_sessions = cursor.fetchall()

    productivity = defaultdict(int)
    for start_str, end_str in all_sessions:
        start = datetime.fromisoformat(start_str)
        end = datetime.fromisoformat(end_str)
        date_key = start.strftime("%Y-%m-%d")
        minutes = int((end - start).total_seconds() // 60)
        productivity[date_key] += minutes

    return render_template('history.html', sessions=sessions, productivity_data=dict(productivity))

@app.route('/pomodoro/start', methods=['POST'])
def pomodoro_start():
    task_id = request.form.get('task_id')
    start_time = datetime.now().isoformat()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sessions (task_id, start_time) VALUES (?, ?)', (task_id, start_time))
        session_id = cursor.lastrowid
    return redirect(url_for('pomodoro_timer', session_id=session_id))

@app.route('/pomodoro/timer/<int:session_id>')
def pomodoro_timer(session_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.id, t.name, s.start_time, s.end_time
            FROM sessions s JOIN tasks t ON s.task_id = t.id
            WHERE s.id = ?
        ''', (session_id,))
        session = cursor.fetchone()
    if not session:
        abort(404)
    return render_template('pomodoro_timer.html', session=session)
 

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
