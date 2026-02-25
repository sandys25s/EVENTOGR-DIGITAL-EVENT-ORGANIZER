import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = 'database/event_organizer.db'

def seed():
    if not os.path.exists(DATABASE):
        print("Database not found. Run force_init.py first.")
        return
    
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    
    # 1. Create Users
    admin_pass = generate_password_hash('admin123')
    user_pass = generate_password_hash('user123')
    
    users = [
        ('Admin User', 'admin@event.com', admin_pass, 'admin'),
        ('Santhosh Kumar', 'user@event.com', user_pass, 'user')
    ]
    
    for user in users:
        cursor.execute("SELECT * FROM users WHERE email = ?", (user[1],))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", user)
            print(f"Added user: {user[1]}")

    # 2. Create Events
    events = [
        (
            'Annual Tech Symposium 2024', 
            'Largest technology festival featuring hackathons, guest lectures, and paper presentations.',
            '2024-05-15', '09:00', 'Main Auditorium', 'Tech', 500.00, 1, 200, '2024-05-10 23:59:00',
            'https://images.unsplash.com/photo-1540575861501-7ad0582373f2?auto=format&fit=crop&q=80&w=800'
        ),
        (
            'Python for Beginners Workshop', 
            'Hands-on workshop for students to learn Python from scratch. Perfect for enthusiasts.',
            '2024-04-20', '14:00', 'Lab 101', 'Workshop', 0.00, 0, 50, '2024-04-18 18:00:00',
            'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&q=80&w=800'
        ),
        (
            'Cultural Fest: Rhythm 2024', 
            'A night of music, dance, and celebrations. Open for all students and guests.',
            '2024-06-01', '18:00', 'Open Air Theatre', 'Cultural', 100.00, 1, 500, '2024-05-28 12:00:00',
            'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?auto=format&fit=crop&q=80&w=800'
        ),
        (
            'AI & Robotics Workshop', 
            'Exploring the future of Artificial Intelligence and its applications in modern Robotics.',
            '2024-05-22', '10:00', 'Seminar Hall B', 'Workshop', 250.00, 1, 100, '2024-05-20 23:59:00',
            'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&q=80&w=800'
        )
    ]
    
    for event in events:
        cursor.execute("SELECT * FROM events WHERE title = ?", (event[0],))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO events (title, description, date, time, venue, category, price, is_paid, max_participants, deadline, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', event)
            print(f"Added event: {event[0]}")
    
    db.commit()
    db.close()
    print("Seeding completed successfully!")

if __name__ == '__main__':
    seed()
