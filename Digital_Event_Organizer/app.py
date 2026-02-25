from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATABASE = os.path.join(os.getcwd(), 'database', 'event_organizer.db')

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    if not os.path.exists('database'):
        os.makedirs('database')
    
    db = get_db()
    with open('database/schema.sql', 'r') as f:
        schema = f.read()
        # Clean up MySQL specific syntax for SQLite
        schema = schema.replace('INT AUTO_INCREMENT PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
        schema = schema.replace('ENUM(\'admin\', \'user\') DEFAULT \'user\'', 'TEXT DEFAULT \'user\'')
        schema = schema.replace('ENUM(\'pending\', \'confirmed\', \'cancelled\') DEFAULT \'pending\'', 'TEXT DEFAULT \'pending\'')
        schema = schema.replace('ENUM(\'unpaid\', \'paid\', \'refunded\') DEFAULT \'unpaid\'', 'TEXT DEFAULT \'unpaid\'')
        schema = schema.replace('ENUM(\'success\', \'failed\', \'pending\') DEFAULT \'pending\'', 'TEXT DEFAULT \'pending\'')
        schema = schema.replace('BOOLEAN DEFAULT FALSE', 'INTEGER DEFAULT 0')
        schema = schema.replace('BOOLEAN DEFAULT TRUE', 'INTEGER DEFAULT 1')
        schema = schema.replace('TIMESTAMP DEFAULT CURRENT_TIMESTAMP', 'DATETIME DEFAULT CURRENT_TIMESTAMP')
        
        db.executescript(schema)
    db.commit()
    db.close()

# Initialize DB on start
if not os.path.exists(DATABASE):
    init_db()

# Helper function to check if user is logged in
def is_logged_in():
    return 'user_id' in session

# Routes
@app.route('/')
def home():
    db = get_db()
    events = db.execute('SELECT * FROM events ORDER BY date ASC LIMIT 6').fetchall()
    db.close()
    return render_template('home.html', events=events)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        db.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['name'] = user['name']
            session['role'] = user['role']
            flash('Logged in successfully!', 'success')
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid email or password', 'error')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = 'user'
        
        hashed_password = generate_password_hash(password)
        
        db = get_db()
        account = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if account:
            flash('Account already exists!', 'error')
        else:
            db.execute('INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)', 
                       (name, email, hashed_password, role))
            db.commit()
            flash('Registration successful! Please login.', 'success')
            db.close()
            return redirect(url_for('login'))
        db.close()
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('user_dashboard'))

# Admin Routes
@app.route('/admin/dashboard')
def admin_dashboard():
    if not is_logged_in() or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    db = get_db()
    events = db.execute('SELECT * FROM events').fetchall()
    user_count = db.execute('SELECT COUNT(*) as count FROM users WHERE role="user"').fetchone()['count']
    reg_count = db.execute('SELECT COUNT(*) as count FROM registrations').fetchone()['count']
    db.close()
    
    return render_template('admin/dashboard.html', events=events, user_count=user_count, reg_count=reg_count)

@app.route('/admin/create_event', methods=['GET', 'POST'])
def create_event():
    if not is_logged_in() or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        time = request.form['time']
        venue = request.form['venue']
        category = request.form['category']
        price = request.form.get('price', 0.00)
        is_paid = 1 if 'is_paid' in request.form else 0
        max_participants = request.form['max_participants']
        deadline = request.form['deadline']
        image_url = request.form.get('image_url', '')

        db = get_db()
        db.execute('''
            INSERT INTO events (title, description, date, time, venue, category, price, is_paid, max_participants, deadline, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, date, time, venue, category, price, is_paid, max_participants, deadline, image_url))
        db.commit()
        db.close()
        flash('Event created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/create_event.html')

@app.route('/admin/edit_event/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    if not is_logged_in() or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    db = get_db()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        time = request.form['time']
        venue = request.form['venue']
        category = request.form['category']
        price = request.form.get('price', 0.00)
        is_paid = 1 if 'is_paid' in request.form else 0
        max_participants = request.form['max_participants']
        deadline = request.form['deadline']
        image_url = request.form.get('image_url', '')

        db.execute('''
            UPDATE events 
            SET title=?, description=?, date=?, time=?, venue=?, category=?, price=?, is_paid=?, max_participants=?, deadline=?, image_url=?
            WHERE event_id=?
        ''', (title, description, date, time, venue, category, price, is_paid, max_participants, deadline, image_url, id))
        db.commit()
        db.close()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    event = db.execute('SELECT * FROM events WHERE event_id = ?', (id,)).fetchone()
    db.close()
    return render_template('admin/edit_event.html', event=event)

@app.route('/admin/delete_event/<int:id>')
def delete_event(id):
    if not is_logged_in() or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    db = get_db()
    db.execute('DELETE FROM events WHERE event_id = ?', (id,))
    db.commit()
    db.close()
    flash('Event deleted successfully!', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/view_participants/<int:id>')
def view_participants(id):
    if not is_logged_in() or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    db = get_db()
    event = db.execute('SELECT title FROM events WHERE event_id = ?', (id,)).fetchone()
    participants = db.execute('''
        SELECT u.name, u.email, r.registration_date, r.status, r.payment_status 
        FROM registrations r 
        JOIN users u ON r.user_id = u.user_id 
        WHERE r.event_id = ?
    ''', (id,)).fetchall()
    db.close()
    
    return render_template('admin/participants.html', participants=participants, event_title=event['title'])

# User Routes
@app.route('/user/dashboard')
def user_dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    db = get_db()
    registrations = db.execute('''
        SELECT r.*, e.title, e.date, e.venue 
        FROM registrations r 
        JOIN events e ON r.event_id = e.event_id 
        WHERE r.user_id = ?
    ''', (user_id,)).fetchall()
    notifications = db.execute('SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
    db.close()
    
    return render_template('user/dashboard.html', registrations=registrations, notifications=notifications)

# Event Routes
@app.route('/events')
def events():
    db = get_db()
    all_events = db.execute('SELECT * FROM events ORDER BY date ASC').fetchall()
    db.close()
    return render_template('events.html', events=all_events)

@app.route('/event/<int:id>')
def event_detail(id):
    db = get_db()
    event = db.execute('SELECT * FROM events WHERE event_id = ?', (id,)).fetchone()
    db.close()
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('home'))
    return render_template('event_detail.html', event=event)

@app.route('/register_event/<int:id>', methods=['POST'])
def register_event(id):
    if not is_logged_in():
        flash('Please login to register.', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    db = get_db()
    
    # Check if already registered
    if db.execute('SELECT * FROM registrations WHERE user_id = ? AND event_id = ?', (user_id, id)).fetchone():
        db.close()
        flash('You are already registered for this event.', 'info')
        return redirect(url_for('event_detail', id=id))
    
    event = db.execute('SELECT * FROM events WHERE event_id = ?', (id,)).fetchone()
    
    if event['current_participants'] >= event['max_participants']:
        db.close()
        flash('Event is full!', 'error')
        return redirect(url_for('event_detail', id=id))
    
    if event['is_paid']:
        db.close()
        return redirect(url_for('payment_mock', event_id=id))
    
    db.execute('INSERT INTO registrations (user_id, event_id, status, payment_status) VALUES (?, ?, ?, ?)',
               (user_id, id, 'confirmed', 'paid'))
    db.execute('UPDATE events SET current_participants = current_participants + 1 WHERE event_id = ?', (id,))
    db.execute('INSERT INTO notifications (user_id, message) VALUES (?, ?)',
               (user_id, f"Successfully registered for {event['title']}!"))
    db.commit()
    db.close()
    flash('Successfully registered for the event!', 'success')
    return redirect(url_for('user_dashboard'))

@app.route('/payment/<int:event_id>', methods=['GET', 'POST'])
def payment_mock(event_id):
    if not is_logged_in():
        return redirect(url_for('login'))
    
    db = get_db()
    event = db.execute('SELECT * FROM events WHERE event_id = ?', (event_id,)).fetchone()
    
    if request.method == 'POST':
        transaction_id = "TXN" + datetime.now().strftime("%Y%m%d%H%M%S")
        user_id = session['user_id']
        
        cursor = db.execute('INSERT INTO registrations (user_id, event_id, status, payment_status) VALUES (?, ?, ?, ?)',
                           (user_id, event_id, 'confirmed', 'paid'))
        reg_id = cursor.lastrowid
        
        db.execute('''
            INSERT INTO payments (registration_id, user_id, amount, transaction_id, payment_status)
            VALUES (?, ?, ?, ?, ?)
        ''', (reg_id, user_id, event['price'], transaction_id, 'success'))
        
        db.execute('UPDATE events SET current_participants = current_participants + 1 WHERE event_id = ?', (event_id,))
        db.execute('INSERT INTO notifications (user_id, message) VALUES (?, ?)',
                   (user_id, f"Payment successful! You are registered for {event['title']}. Transaction ID: {transaction_id}"))
        
        db.commit()
        db.close()
        flash(f'Payment successful! Transaction ID: {transaction_id}', 'success')
        return redirect(url_for('user_dashboard'))
    
    db.close()
    return render_template('payment.html', event=event)

if __name__ == '__main__':
    app.run(debug=True)
