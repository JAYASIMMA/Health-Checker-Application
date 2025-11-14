# 🏥 Health Checker AI - Complete Setup Guide

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![Ollama](https://img.shields.io/badge/Ollama-Latest-purple.svg)

**AI-Powered Health Symptom Analyzer using Jemma-AI Model**

</div>

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Prerequisites](#prerequisites)
5. [Installation Guide](#installation-guide)
6. [Project Structure](#project-structure)
7. [Configuration](#configuration)
8. [Running the Application](#running-the-application)
9. [Usage Guide](#usage-guide)
10. [Troubleshooting](#troubleshooting)
11. [API Documentation](#api-documentation)
12. [Security Considerations](#security-considerations)
13. [Contributing](#contributing)
14. [License](#license)

---

## 🎯 Overview

**Health Checker AI** is a sophisticated web application that leverages artificial intelligence to provide preliminary health insights based on user-reported symptoms. Powered by the advanced **Jemma-AI model** running on **Ollama**, this platform offers quick, AI-driven health assessments with medication recommendations.

### ⚠️ Important Disclaimer

This application is **NOT** a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

---

## ✨ Features

### Core Functionality
- 🤖 **AI-Powered Analysis** - Utilizes Jemma-AI for intelligent symptom assessment
- 📊 **Health History Tracking** - Comprehensive record of all consultations
- 👤 **User Profile Management** - Personal dashboard with statistics
- 💊 **Medication Recommendations** - Suggests over-the-counter tablets when applicable
- 🔒 **Secure Authentication** - SHA-256 password hashing
- 📱 **Responsive Design** - Works seamlessly on all devices
- 🎨 **Professional UI** - Clean, medical-grade interface with Bootstrap 5

### Advanced Features
- ✅ **Formatted Responses** - Professional medical-style output with bold headings and bullet points
- ✅ **Real-time Processing** - Fast AI response times
- ✅ **Session Management** - Secure user sessions
- ✅ **Error Handling** - Comprehensive error management
- ✅ **Database Integration** - Persistent data storage with MySQL

---

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Python web framework
- **PyMySQL 1.1.0** - MySQL database connector
- **Python 3.8+** - Programming language

### Database
- **MySQL 8.0+** - Relational database (via XAMPP)
- **phpMyAdmin** - Database management interface

### AI/ML
- **Ollama** - Local AI model server
- **Jemma-AI** - Medical AI model by Jayasimma

### Frontend
- **Bootstrap 5.3.0** - CSS framework
- **Font Awesome 6.4.0** - Icon library
- **Jinja2** - Template engine

### Security
- **Hashlib** - SHA-256 password encryption
- **Flask Sessions** - Secure session management

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

### 1. XAMPP
- **Version**: 8.0 or higher
- **Download**: [https://www.apachefriends.org/](https://www.apachefriends.org/)
- **Components Needed**: Apache, MySQL, phpMyAdmin

### 2. Python
- **Version**: 3.8 or higher
- **Download**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **Add to PATH**: Make sure Python is added to system PATH

### 3. Ollama
- **Download**: [https://ollama.ai/](https://ollama.ai/)
- **Installation**: Follow platform-specific instructions
- **Required for**: Running the Jemma-AI model

### 4. Git (Optional)
- **Download**: [https://git-scm.com/](https://git-scm.com/)
- **Used for**: Cloning the repository

---

## 🚀 Installation Guide

### Step 1: Install and Configure Ollama

#### Windows
```bash
# Download and install Ollama from https://ollama.ai/

# Open Command Prompt or PowerShell
# Pull the Jemma-AI model
ollama pull Jayasimma/jemma-ai

# Verify the model is installed
ollama list

# Start Ollama server (if not running automatically)
ollama serve
```

#### macOS
```bash
# Install Ollama
brew install ollama

# Pull the model
ollama pull Jayasimma/jemma-ai

# Start the server
ollama serve
```

#### Linux
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the model
ollama pull Jayasimma/jemma-ai

# Start the server
ollama serve
```

**Verify Installation:**
```bash
# Test the API
curl http://localhost:11434/api/generate -d '{
  "model": "Jayasimma/jemma-ai",
  "prompt": "Hello"
}'
```

---

### Step 2: Setup XAMPP and MySQL Database

#### 2.1 Start XAMPP Services

1. **Open XAMPP Control Panel**
2. **Start Apache** - Click "Start" button next to Apache
3. **Start MySQL** - Click "Start" button next to MySQL
4. **Verify Services** - Both should show green "Running" status

#### 2.2 Create Database

**Option A: Using phpMyAdmin (Recommended)**

1. Open browser and go to `http://localhost/phpmyadmin`
2. Click on "New" in the left sidebar
3. Enter database name: `health_checker_db`
4. Select collation: `utf8mb4_unicode_ci`
5. Click "Create"

**Option B: Using MySQL Command Line**

```bash
# Open MySQL command line from XAMPP
mysql -u root -p

# Create database
CREATE DATABASE health_checker_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Verify database
SHOW DATABASES;

# Exit
EXIT;
```

#### 2.3 Import Database Schema

**Method 1: Using phpMyAdmin**

1. Go to `http://localhost/phpmyadmin`
2. Select `health_checker_db` from left sidebar
3. Click "Import" tab
4. Click "Choose File" and select `database.sql`
5. Scroll down and click "Go"
6. You should see "Import has been successfully finished"

**Method 2: Using SQL Tab**

1. Go to `http://localhost/phpmyadmin`
2. Select `health_checker_db`
3. Click "SQL" tab
4. Copy and paste the following SQL:

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS health_checker_db;
USE health_checker_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Health checks table
CREATE TABLE IF NOT EXISTS health_checks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    symptoms TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

5. Click "Go"

**Verify Tables:**
```sql
-- Check if tables are created
SHOW TABLES;

-- Check users table structure
DESCRIBE users;

-- Check health_checks table structure
DESCRIBE health_checks;
```

---

### Step 3: Setup Python Environment

#### 3.1 Create Project Directory

```bash
# Create project folder
mkdir health_checker_app
cd health_checker_app
```

#### 3.2 Create Virtual Environment (Recommended)

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your command prompt
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal
```

#### 3.3 Install Dependencies

```bash
# Make sure virtual environment is activated
# Install all required packages
pip install Flask==3.0.0
pip install PyMySQL==1.1.0
pip install requests==2.31.0
pip install cryptography==41.0.7

# Or use requirements.txt
pip install -r requirements.txt
```

**Verify Installation:**
```bash
# List installed packages
pip list

# Should show:
# Flask         3.0.0
# PyMySQL       1.1.0
# requests      2.31.0
# cryptography  41.0.7
```

---

### Step 4: Configure the Application

#### 4.1 Update Database Configuration

Open `app.py` and update the database credentials:

```python
# Database configuration for XAMPP MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Leave empty for default XAMPP, or enter your MySQL password
    'database': 'health_checker_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
```

**If you set a MySQL password:**
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YourPasswordHere',  # Your actual password
    'database': 'health_checker_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
```

#### 4.2 Change Secret Key (IMPORTANT for Security)

```python
# Generate a secure random secret key
import secrets
print(secrets.token_hex(32))

# Copy the output and paste it here:
app.secret_key = 'your_generated_secret_key_here'
```

#### 4.3 Verify Ollama Configuration

```python
# Ollama API configuration
OLLAMA_API_URL = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = 'Jayasimma/jemma-ai'

# Change port if your Ollama runs on different port
```

---

## 📁 Project Structure

Create the following folder structure:

```
health_checker_app/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── database.sql               # Database schema
├── README.md                  # This file
│
├── templates/                 # HTML templates folder (MUST CREATE)
│   ├── base.html             # Base template with navigation
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── health_checker.html   # Main health check page
│   ├── history.html          # History page
│   ├── profile.html          # User profile page
│   └── about.html            # About page
│
├── static/                    # Static files folder (Optional)
│   ├── css/                  # Custom CSS files
│   ├── js/                   # Custom JavaScript files
│   └── images/               # Images and logos
│
└── venv/                     # Virtual environment (auto-created)
```

**Create Templates Folder:**
```bash
# In your project directory
mkdir templates

# Verify
ls -la  # or 'dir' on Windows
```

---

## ⚙️ Configuration

### Environment Variables (Optional but Recommended)

Create a `.env` file for sensitive configuration:

```bash
# .env file
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=health_checker_db
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=Jayasimma/jemma-ai
```

**Load environment variables in app.py:**
```python
from dotenv import load_dotenv
import os

load_dotenv()

app.secret_key = os.getenv('SECRET_KEY')
```

---

## 🎮 Running the Application

### Step 1: Start Required Services

**Check Service Status:**

1. **XAMPP Services**
   - Apache: ✅ Running (Green)
   - MySQL: ✅ Running (Green)

2. **Ollama Server**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # If not running, start it
   ollama serve
   ```

### Step 2: Activate Virtual Environment

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Run Flask Application

```bash
# Make sure you're in the project directory
# Run the application
python app.py

# You should see:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

### Step 4: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

**Expected Behavior:**
- Should redirect to login page
- No errors in the console
- Page loads successfully

---

## 📖 Usage Guide

### First Time Setup

#### 1. Register a New Account

1. Click "Register" button on login page
2. Fill in the registration form:
   - **Username**: Choose a unique username
   - **Email**: Enter valid email address
   - **Password**: Minimum 6 characters
   - **Confirm Password**: Must match password
3. Click "Register"
4. Success message: "Registration successful! Please login."

#### 2. Login

1. Enter your email and password
2. Click "Login"
3. Redirects to Health Checker page

### Using Health Checker

#### 1. Enter Symptoms

```
Example Input:
"I have a severe headache, fever of 101°F, and body aches for the past 2 days"
```

#### 2. Get AI Analysis

- Click "Analyze Symptoms"
- Wait for AI processing (5-30 seconds)
- View formatted response with:
  - **Brief Analysis**
  - **Possible Conditions**
  - **Medication Recommendations**
  - **When to Seek Medical Attention**

#### 3. View Response Format

The AI response will be professionally formatted:

```
1. Brief Analysis of the Symptoms:
[AI analysis here with bold headings]

2. Possible Conditions (Not a Diagnosis):
• Condition 1: Description
• Condition 2: Description
• Condition 3: Description

3. General Recommendations and Medications:
• Medication recommendations
• General care instructions

4. When to Seek Medical Attention:
[Warning signs listed]
```

### Viewing History

1. Click "History" in navigation
2. See all previous health checks
3. Click on any item to expand full details
4. Responses are stored with original formatting

### Managing Profile

1. Click "Profile" in navigation
2. View account information:
   - Username
   - Email
   - Member since date
   - Total health checks
3. Quick action buttons:
   - New Health Check
   - View History
   - About the App
   - Logout

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Error

**Error Message:**
```
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")
```

**Solutions:**
- ✅ Check if MySQL is running in XAMPP Control Panel
- ✅ Verify database credentials in `app.py`
- ✅ Test connection:
  ```bash
  mysql -u root -p -h localhost
  ```
- ✅ Check if database exists:
  ```sql
  SHOW DATABASES;
  ```

#### 2. Ollama Connection Error

**Error Message:**
```
Error connecting to Ollama: Connection refused
```

**Solutions:**
- ✅ Check if Ollama is running:
  ```bash
  curl http://localhost:11434/api/tags
  ```
- ✅ Start Ollama server:
  ```bash
  ollama serve
  ```
- ✅ Verify model is installed:
  ```bash
  ollama list
  ```
- ✅ Pull model if missing:
  ```bash
  ollama pull Jayasimma/jemma-ai
  ```

#### 3. Template Not Found Error

**Error Message:**
```
jinja2.exceptions.TemplateNotFound: health_checker.html
```

**Solutions:**
- ✅ Create `templates` folder in project root
- ✅ Ensure all HTML files are in `templates/` folder
- ✅ Check file names match exactly (case-sensitive)
- ✅ Verify folder structure:
  ```
  health_checker_app/
  ├── app.py
  └── templates/
      ├── base.html
      ├── login.html
      └── ...
  ```

#### 4. Port Already in Use

**Error Message:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**
- ✅ Stop any running Flask applications
- ✅ Change port in `app.py`:
  ```python
  app.run(debug=True, port=5001)  # Use different port
  ```
- ✅ Kill process using port 5000 (Windows):
  ```bash
  netstat -ano | findstr :5000
  taskkill /PID [PID_NUMBER] /F
  ```
- ✅ Kill process (macOS/Linux):
  ```bash
  lsof -ti:5000 | xargs kill -9
  ```

#### 5. Import Error

**Error Message:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solutions:**
- ✅ Activate virtual environment
- ✅ Reinstall dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- ✅ Verify installation:
  ```bash
  pip list
  ```

#### 6. CSS/Styling Not Loading

**Solutions:**
- ✅ Hard refresh browser: `Ctrl + Shift + R` (or `Cmd + Shift + R`)
- ✅ Clear browser cache
- ✅ Check browser console for errors (F12)
- ✅ Verify Bootstrap CDN is accessible

#### 7. AI Response Not Formatting

**Problem:** Response shows `**text**` instead of bold

**Solutions:**
- ✅ Verify `| safe` filter is used in templates:
  ```html
  {{ response | safe }}
  ```
- ✅ Check `format_response()` function in `app.py`
- ✅ Clear browser cache

---

## 📡 API Documentation

### Internal API Endpoints

#### User Authentication

**Register User**
```http
POST /register
Content-Type: application/x-www-form-urlencoded

username=johndoe&email=john@example.com&password=secret123&confirm_password=secret123
```

**Response:**
- Success: Redirect to `/login` with success message
- Error: Redirect to `/register` with error message

**Login User**
```http
POST /login
Content-Type: application/x-www-form-urlencoded

email=john@example.com&password=secret123
```

**Response:**
- Success: Redirect to `/health-checker`, sets session
- Error: Redirect to `/login` with error message

**Logout User**
```http
GET /logout
```

**Response:**
- Clears session
- Redirect to `/login`

#### Health Check

**Create Health Check**
```http
POST /health-checker
Content-Type: application/x-www-form-urlencoded
Authorization: Session Required

symptoms=headache and fever
```

**Response:**
- Renders `health_checker.html` with AI response
- Saves to database

#### View History

**Get User History**
```http
GET /history
Authorization: Session Required
```

**Response:**
- Renders `history.html` with list of health checks
- Returns last 50 records

#### User Profile

**Get Profile**
```http
GET /profile
Authorization: Session Required
```

**Response:**
- Renders `profile.html` with user data and statistics

### Ollama API Integration

**Generate Response**
```python
payload = {
    "model": "Jayasimma/jemma-ai",
    "prompt": "User symptoms here",
    "stream": False
}

response = requests.post(
    "http://localhost:11434/api/generate",
    json=payload,
    timeout=60
)
```

**Response Format:**
```json
{
  "model": "Jayasimma/jemma-ai",
  "created_at": "2024-01-01T00:00:00Z",
  "response": "AI generated response here",
  "done": true
}
```

---

## 🔐 Security Considerations

### Production Deployment Checklist

#### 1. Change Secret Key
```python
# Generate strong secret key
import secrets
app.secret_key = secrets.token_hex(32)
```

#### 2. Disable Debug Mode
```python
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

#### 3. Use Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
```

#### 4. Enable HTTPS
- Use SSL/TLS certificates
- Implement HTTPS redirects
- Use secure cookies

#### 5. Database Security
- Change MySQL root password
- Create dedicated database user
- Use strong passwords
- Enable SQL injection protection

#### 6. Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic
```

#### 7. Input Validation
- Sanitize all user inputs
- Validate email formats
- Check password strength
- Prevent XSS attacks

#### 8. Session Security
```python
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1)
)
```

### Password Security

**Current Implementation:**
- SHA-256 hashing
- Salt: None (consider adding)

**Recommended Enhancement:**
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hash password
hashed = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

# Verify password
check_password_hash(hashed, password)
```

---

## 🐛 Known Issues

1. **Large Response Times**
   - AI processing can take 30-60 seconds
   - Consider implementing async processing

2. **Mobile Responsiveness**
   - Some tables may overflow on small screens
   - Horizontal scrolling implemented

3. **Browser Compatibility**
   - Tested on Chrome, Firefox, Edge
   - Safari may have minor CSS differences

---

## 🚀 Future Enhancements

### Planned Features
- [ ] Email verification for registration
- [ ] Password reset functionality
- [ ] Export health history to PDF
- [ ] Multi-language support
- [ ] Voice input for symptoms
- [ ] Doctor appointment booking
- [ ] Medicine reminders
- [ ] Health data analytics dashboard
- [ ] Integration with wearable devices
- [ ] Telemedicine consultation booking

### Technical Improvements
- [ ] Implement Redis for caching
- [ ] Add unit tests
- [ ] API rate limiting
- [ ] WebSocket for real-time updates
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Load balancing
- [ ] Database replication

---

## 📞 Support

### Getting Help

1. **Check Troubleshooting Section** - Most common issues are covered
2. **Review Error Messages** - Flask provides detailed error traces
3. **Check Logs** - Flask console output shows detailed information
4. **Verify Prerequisites** - Ensure all services are running

### Debug Mode

Enable detailed error messages:
```python
app.run(debug=True)
```

Access Flask debugger in browser when errors occur.

---

## 📄 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2024 Health Checker AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

- **Ollama** - For providing the AI model serving platform
- **Jayasimma** - For the Jemma-AI medical model
- **Flask** - Web framework
- **Bootstrap** - UI framework
- **Font Awesome** - Icons

---

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.15+, Ubuntu 20.04+
- **RAM**: 8 GB
- **Storage**: 10 GB free space
- **Processor**: Intel i5 or equivalent
- **Internet**: Stable connection for model downloads

### Recommended Requirements
- **OS**: Windows 11, macOS 12+, Ubuntu 22.04+
- **RAM**: 16 GB or more
- **Storage**: 20 GB free space (SSD preferred)
- **Processor**: Intel i7 or equivalent
- **GPU**: Optional, for faster AI processing

---

## 📝 Version History

### Version 1.0.0 (Current)
- Initial release
- User authentication system
- Health symptom analyzer
- History tracking
- Profile management
- Responsive UI
- Professional formatting

---

## 🎓 Learning Resources

### Flask
- [Flask Official Documentation](https://flask.palletsprojects.com/)
- [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

### Ollama
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)

### MySQL
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)

---

**Made with ❤️ by Jayasimma & AI Team**

**Last Updated**: 2024
**Version**: 1.0.0