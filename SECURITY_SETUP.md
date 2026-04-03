# 🔐 PERMANENT DOMAIN & SECURITY SETUP GUIDE

## 📋 What's Enhanced:

✅ **Security Features Added:**
- Session management (24-hour sessions)
- Rate limiting (5 login attempts per minute)
- Strong password requirements (8+ chars, uppercase, lowercase, digit, special char)
- HTTPS-only cookies (when using HTTPS via ngrok)
- CSRF protection enabled
- Secure password hashing (PBKDF2-SHA256)

✅ **Login Protection:**
- Automatic account lockout after repeated failed attempts
- Secure session cookies
- Logout functionality

---

## 🌐 SETUP: PERMANENT DOMAIN WITH NGROK

### Option 1: Free Tier (Changes URL every time)

1. **Start your app:**
   ```bash
   pip install -r requirements.txt
   python chat_app.py
   ```

2. **In new terminal, start ngrok:**
   ```bash
   ngrok http 5000 --auth "login:password123"
   ```

3. **Share public URL** - Changes each time you restart

---

### Option 2: Pro Plan (PERMANENT DOMAIN - Recommended)

#### Step 1: Create ngrok Account
1. Go to: https://ngrok.com
2. Sign up (free account)
3. Get your **Auth Token** from: https://dashboard.ngrok.com/auth

#### Step 2: Connect ngrok to Your Computer
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

#### Step 3: Get Permanent Domain (Pro Plan)
1. Upgrade to Pro: https://ngrok.com/pricing
2. In ngrok Dashboard → Domains → Reserve a domain
3. Example: `my-private-chat.ngrok.io`

#### Step 4: Update ngrok Config
Edit `.ngrok.yml` and replace:
```yaml
domain: my-private-chat.ngrok.io  # Your permanent domain
```

#### Step 5: Start App & ngrok
```bash
# Terminal 1: Start Flask app
python chat_app.py

# Terminal 2: Start ngrok (reads config automatically)
ngrok start chat_app
```

#### Step 6: Access from Anywhere
```
https://my-private-chat.ngrok.io
```
Username: `login`
Password: `password123`

---

## 🔒 PASSWORD REQUIREMENTS

When users register, passwords must have:
- ✅ Minimum 8 characters
- ✅ At least 1 UPPERCASE letter
- ✅ At least 1 lowercase letter
- ✅ At least 1 number (0-9)
- ✅ At least 1 special character (!@#$%^&*)

**Example valid password:** `SecurePass123!`

---

## 🛡️ SECURITY BEST PRACTICES

### For Both Users:
1. **Use strong, unique passwords**
2. **Log out** when done
3. **Don't share your account**
4. **Only access via HTTPS link** (ngrok provides this automatically)

### For Public Deployment:
1. **Enable authentication in ngrok:**
   ```bash
   ngrok http 5000 --auth "username:password"
   ```

2. **Use IP whitelist** (edit `.ngrok.yml`):
   ```yaml
   allowed_ips:
     - "1.2.3.4"  # Your girlfriend's IP
   ```

3. **Monitor ngrok dashboard** for suspicious access

---

## 📱 ACCESSING FROM HER DEVICE

**Desktop/Laptop:**
1. Open browser
2. Go to: `https://my-private-chat.ngrok.io`
3. Register or login

**Mobile (iPhone/Android):**
1. Open Safari/Chrome
2. Go to: `https://my-private-chat.ngrok.io`
3. Add to homescreen for easy access

---

## 🚀 PRODUCTION DEPLOYMENT

For a truly permanent solution, consider:

1. **Railway.app** (Free tier available)
2. **Render.com** (Free tier available)
3. **AWS/Azure** (More complex, more expensive)
4. **Custom domain + Cloudflare** (Advanced)

---

## ❓ TROUBLESHOOTING

**"Invalid username or password"**
- Check username spelling
- Ensure password is correct
- Try registering a new account

**"Connection refused"**
- Make sure `python chat_app.py` is running
- Check port 5000 is not blocked
- Try restarting the app

**"ngrok not found"**
- Install: `choco install ngrok` (Windows)
- Or download from https://ngrok.com/download

**URL keeps changing**
- This is normal for free tier
- Upgrade to Pro for permanent domain

---

## 📞 QUICK START CHECKLIST

- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Run Flask app: `python chat_app.py`
- [ ] Download ngrok from ngrok.com
- [ ] Create ngrok account & get auth token
- [ ] Configure ngrok with: `ngrok config add-authtoken YOUR_TOKEN`
- [ ] Update `.ngrok.yml` with your domain
- [ ] Start ngrok: `ngrok start chat_app`
- [ ] Share URL with girlfriend
- [ ] Both register accounts with strong passwords
- [ ] Start chatting! 💕

---

**Need help?** Check ngrok docs: https://ngrok.com/docs
