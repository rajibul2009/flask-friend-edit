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
                        name TEXT NOT NULL,
                        school_name TEXT NOT NULL,
                        birth_date null,
                        profession TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        blood_group TEXT NOT NULL,
                        tshirt_size TEXT NOT NULL,
                        email TEXT null,
                        current_address TEXT NOT NULL,
                        permanent_address TEXT NOT NULL
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
    # ফর্ম ডেটা সংগ্রহ
    name = request.form['name']
    school_name = request.form['school_name']
    birth_date = request.form['birth_date']
    profession = request.form['profession']
    phone = request.form['phone']
    blood_group = request.form['blood_group']
    tshirt_size = request.form['tshirt_size']
    email = request.form['email']
    current_address = request.form['current_address']
    permanent_address = request.form['permanent_address']

    # ডাটাবেসে বন্ধুদের তথ্য সংরক্ষণ
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO friends 
                    (name, school_name, birth_date, profession, phone, 
                    blood_group, tshirt_size, email, current_address, permanent_address)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (name, school_name, birth_date, profession, phone,
                    blood_group, tshirt_size, email, current_address, permanent_address))
    conn.commit()

    return redirect(url_for('index'))

# বন্ধু এডিট করার ফাংশন
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        # আপডেট করা ডেটা সংগ্রহ
        name = request.form['name']
        school_name = request.form['school_name']
        birth_date = request.form['birth_date']
        profession = request.form['profession']
        phone = request.form['phone']
        blood_group = request.form['blood_group']
        tshirt_size = request.form['tshirt_size']
        email = request.form['email']
        current_address = request.form['current_address']
        permanent_address = request.form['permanent_address']

        # ডাটাবেস আপডেট
        cursor.execute('''UPDATE friends SET 
                        name = ?, school_name = ?, birth_date = ?, profession = ?, 
                        phone = ?, blood_group = ?, tshirt_size = ?, email = ?, 
                        current_address = ?, permanent_address = ?
                        WHERE id = ?''',
                        (name, school_name, birth_date, profession,
                        phone, blood_group, tshirt_size, email,
                        current_address, permanent_address, id))
        conn.commit()

        return redirect(url_for('index'))

    # এডিট ফর্মে ডেটা লোড
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

# এক্সেল ফাইল ডাউনলোড
@app.route('/download_excel')
def download_excel():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM friends")
    friends = cursor.fetchall()

    # ডাটাফ্রেম তৈরি
    df = pd.DataFrame(friends, columns=[
        'ID', 'Name', 'School', 'Birthdate', 'Profession',
        'Phone', 'Blood Group', 'T-Shirt Size', 'Email',
        'Current Address', 'Permanent Address'
    ])

    # এক্সেল ফাইল তৈরি
    file_path = 'friends_list.xlsx'
    df.to_excel(file_path, index=False, engine='openpyxl')

    # ফাইল ডাউনলোড
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

    from datetime import datetime

    @app.route('/')
    def index():
        current_year = datetime.now().year
        # Your existing code to get friends
        return render_template('index.html', friends=friends, current_year=current_year)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
