from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import os
import pandas as pd

app = Flask(__name__)

# SQLite ডাটাবেসের পাথ
DATABASE = 'friends.db'

# ডাটাবেসের সাথে সংযোগ
def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# ডাটাবেসে টেবিল তৈরি করা
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS friends (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        school_name TEXT,
                        birth_date TEXT,
                        profession TEXT,
                        phone TEXT,
                        email TEXT,
                        current_address TEXT,
                        permanent_address TEXT
                    )''')
    conn.commit()

# ডাটাবেসের সকল বন্ধুদের তথ্য দেখানো
@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM friends")
    friends = cursor.fetchall()
    return render_template('index.html', friends=friends)

# নতুন বন্ধু যোগ করার জন্য ফর্ম
@app.route('/', methods=['POST'])
def add_friend():
    name = request.form['name']
    school_name = request.form['school_name']
    birth_date = request.form['birth_date']
    profession = request.form['profession']
    phone = request.form['phone']
    email = request.form['email']
    current_address = request.form['current_address']
    permanent_address = request.form['permanent_address']

    # ডাটাবেসে বন্ধুদের তথ্য সংরক্ষণ করা
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO friends (name, school_name, birth_date, profession, phone, email, current_address, permanent_address)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (name, school_name, birth_date, profession, phone, email, current_address, permanent_address))
    conn.commit()

    return redirect(url_for('index'))

# বন্ধু এডিট করার ফাংশন
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        school_name = request.form['school_name']
        birth_date = request.form['birth_date']
        profession = request.form['profession']
        phone = request.form['phone']
        email = request.form['email']
        current_address = request.form['current_address']
        permanent_address = request.form['permanent_address']

        cursor.execute('''UPDATE friends SET name = ?, school_name = ?, birth_date = ?, profession = ?, phone = ?, email = ?, current_address = ?, permanent_address = ?
                          WHERE id = ?''',
                          (name, school_name, birth_date, profession, phone, email, current_address, permanent_address, id))
        conn.commit()

        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM friends WHERE id = ?", (id,))
    friend = cursor.fetchone()

    return render_template('edit.html', friend=friend)

# বন্ধু মুছে ফেলার ফাংশন
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM friends WHERE id = ?", (id,))
    conn.commit()
    return redirect(url_for('index'))

# এক্সেল ফাইল ডাউনলোড করার ফাংশন
# @app.route('/download_excel')
# def download_excel():
#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM friends")
#     friends = cursor.fetchall()
#
#     # ডাটাকে pandas DataFrame এ রূপান্তর করা
#     df = pd.DataFrame(friends, columns=['ID','Name', 'School', 'Birthdate', 'Profession', 'Phone', 'Email', 'Current Address', 'Permanent Address'])
#
#     # এক্সেল ফাইল তৈরি করা
#     file_path = 'friends_list.xlsx'
#     df.to_excel(file_path, index=False, engine='openpyxl')
#
#     # এক্সেল ফাইল ডাউনলোড করার জন্য প্রস্তাব
#     return send_file(file_path, as_attachment=True)

@app.route('/download_excel')
def download_excel():
    # ডাটাবেস থেকে ডাটা নিয়ে আসা
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM friends")
    friends = cursor.fetchall()

    # ডাটাকে pandas DataFrame এ রূপান্তর করা
    df = pd.DataFrame(friends, columns=['ID','Name', 'School', 'Birthdate', 'Profession', 'Phone', 'Email', 'Current Address', 'Permanent Address'])

    # এক্সেল ফাইল তৈরি করা
    file_path = 'friends_list.xlsx'
    df.to_excel(file_path, index=False, engine='openpyxl')

    # ফাইল ক্লায়েন্টকে পাঠানো
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404
@app.route('/')
def home():
    return "Hello, বন্ধু! এটা Render থেকে লাইভ চলছে!"

@app.route('/edit')
def edit_friend():
    return render_template('edit.html')


if __name__ == "__main__":

    init_db()  # অ্যাপ শুরু হওয়ার সময় ডাটাবেস ইনিশিয়ালাইজ করা
    app.run(debug=True)
