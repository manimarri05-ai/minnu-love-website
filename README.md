# 🔐 Private Chat App

A beautiful, feature-rich private chat application built with Flask and modern web technologies.

## ✨ Features

- **User Authentication**: Secure login & registration system
- **Real-time Messaging**: Instant message exchange (updates every 2 seconds)
- **File Sharing**: Upload and download files/images with messages
- **Emoji Support**: Express yourself with 18+ emojis
- **Persistent Storage**: All messages are saved to a SQLite database
- **Beautiful UI**: Modern, responsive design with smooth animations
- **Network Ready**: Can be accessed over network (change host in settings)

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python chat_app.py
```

The app will start at `http://localhost:5000`

### Step 3: Create Account & Chat
1. Go to http://localhost:5000 in your browser
2. Click "Create Account" to register (or login with existing account)
3. Enter a username and password
4. Once logged in, select a contact from the list to start chatting

## 🔧 Configuration

### For Network Access
If you want to access this from another computer on your network:

Edit `chat_app.py` and change this line:
```python
app.run(host='127.0.0.1', port=5000, debug=True)
```

To:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

Then access it from another computer using: `http://YOUR_IP:5000`

## 📁 Project Structure

```
app.py/
├── chat_app.py          # Flask backend server
├── templates/
│   └── chat.html        # Frontend UI (HTML/CSS/JS)
├── uploads/             # Uploaded files storage
├── chat.db              # SQLite database (auto-created)
└── requirements.txt     # Python dependencies
```

## 🎮 How to Use

1. **Register**: Create a new account with username and password
2. **View Contacts**: See all other registered users in the sidebar
3. **Select Contact**: Click on any contact to open chat
4. **Send Messages**: Type and press Enter or click Send
5. **Add Emojis**: Click 😀 button to insert emojis
6. **Share Files**: Click 📎 button to upload files/images
7. **Download Files**: Click on file links to download

## 🔒 Security Notes

- Passwords are hashed using Werkzeug security
- Change the SECRET_KEY in `chat_app.py` before deployment
- Messages are stored in SQLite database
- Maximum file upload size: 16MB

## 🐛 Troubleshooting

**Port 5000 already in use?**
- Change the port number in `chat_app.py` to something like 5001

**Can't see the app?**
- Make sure Flask is installed: `pip install Flask Flask-CORS`
- Check if the server is running

**File upload not working?**
- Make sure the `uploads` folder exists
- Check file size (max 16MB)

## 📝 Features Coming Soon

- End-to-end encryption
- Voice/video calls
- Message reactions
- Typing indicators
- Message search

## 📄 License

Personal/Private use only.

Enjoy your private chats! 💬
