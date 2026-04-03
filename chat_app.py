import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

app = Flask(__name__)
CORS(app)

# Static files configuration
app.config['STATIC_FOLDER'] = 'static'
app.config['TEMPLATES_FOLDER'] = 'templates'

# Security Configuration
import secrets
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Generate secure random key
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Rate limiting for login protection
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id TEXT PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    
    # Messages table
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id TEXT PRIMARY KEY, sender_id TEXT, receiver_id TEXT, 
                  message TEXT, message_type TEXT, file_path TEXT, 
                  timestamp TEXT, FOREIGN KEY(sender_id) REFERENCES users(id),
                  FOREIGN KEY(receiver_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

init_db()

# User management
def validate_password(password):
    """Validate password strength (min 8 chars, upper, lower, digit, special)"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain digit"
    if not any(c in '!@#$%^&*' for c in password):
        return False, "Password must contain special char (!@#$%^&*)"
    return True, "Password valid"

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    # Validation
    if not username or len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    
    if not password:
        return jsonify({'error': 'Password required'}), 400
    
    is_valid, message = validate_password(password)
    if not is_valid:
        return jsonify({'error': message}), 400
    
    user_id = str(uuid.uuid4())
    hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
    
    try:
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        c.execute('INSERT INTO users VALUES (?, ?, ?)', (user_id, username, hashed_pw))
        conn.commit()
        conn.close()
        
        # Auto-login after registration
        session.permanent = True
        session['user_id'] = user_id
        session['username'] = username
        
        return jsonify({'success': True, 'user_id': user_id, 'username': username})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limit login attempts
def login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user and check_password_hash(user[1], password):
        session.permanent = True
        session['user_id'] = user[0]
        session['username'] = username
        return jsonify({'success': True, 'user_id': user[0], 'username': username})
    
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/users', methods=['GET'])
def get_users():
    current_user_id = request.args.get('user_id')
    
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('SELECT id, username FROM users WHERE id != ?', (current_user_id,))
    users = [{'id': row[0], 'username': row[1]} for row in c.fetchall()]
    conn.close()
    
    return jsonify(users)

# Chat messages
@app.route('/api/messages', methods=['GET'])
def get_messages():
    user1_id = request.args.get('user1_id')
    user2_id = request.args.get('user2_id')
    
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''SELECT id, sender_id, message, message_type, file_path, timestamp 
                 FROM messages 
                 WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
                 ORDER BY timestamp ASC''',
              (user1_id, user2_id, user2_id, user1_id))
    
    messages = []
    for row in c.fetchall():
        messages.append({
            'id': row[0],
            'sender_id': row[1],
            'message': row[2],
            'message_type': row[3],
            'file_path': row[4],
            'timestamp': row[5]
        })
    
    conn.close()
    return jsonify(messages)

@app.route('/api/messages', methods=['POST'])
def send_message():
    sender_id = request.form.get('sender_id')
    receiver_id = request.form.get('receiver_id')
    message_text = request.form.get('message')
    message_type = request.form.get('message_type', 'text')
    
    msg_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    file_path = None
    
    if message_type == 'file' and 'file' in request.files:
        file = request.files['file']
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            message_text = filename
    
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?)',
              (msg_id, sender_id, receiver_id, message_text, message_type, file_path, timestamp))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'msg_id': msg_id})

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = secure_filename(filename)
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], file_path), as_attachment=True)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/minnu')
def 
# Navigate to your project

minnu():
    response = app.make_response(render_template('html/minnu.html'))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    # Run on all network interfaces for network access
    app.run(host='0.0.0.0', port=5000, debug=True)
