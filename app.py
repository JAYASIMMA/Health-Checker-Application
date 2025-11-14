from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pymysql
import hashlib
import requests
import json
import re
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_this'  # Change this to a random secret key

# Database configuration for XAMPP MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Momdad2004',
    'database': 'health_checker_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Ollama API configuration
OLLAMA_API_URL = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = 'Jayasimma/jemma-ai'

# Database connection helper
def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Format markdown-like text to HTML
def format_response(text):
    """Convert markdown-style formatting to HTML with professional medical formatting"""
    if not text:
        return ""
    
    # First, handle bold text with ** (must be done before italic)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Handle italic text with single * (only if not part of list markers)
    # This regex looks for * that is not preceded or followed by another *
    text = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', text)
    
    # Split into lines for processing
    lines = text.split('\n')
    formatted_lines = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines but add spacing
        if not stripped:
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            formatted_lines.append('<div class="spacing"></div>')
            continue
        
        # Check for bullet points (starting with * or -)
        if re.match(r'^[\*\-]\s+', stripped):
            if not in_list:
                formatted_lines.append('<ul class="formatted-list">')
                in_list = True
            # Remove the marker (* or -) and create list item
            content = re.sub(r'^[\*\-]\s+', '', stripped)
            formatted_lines.append(f'<li>{content}</li>')
        
        # Check for numbered sections like "1.", "2.", "3.", etc.
        elif re.match(r'^\d+\.\s+', stripped):
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            formatted_lines.append(f'<div class="section-heading">{stripped}</div>')
        
        # Regular paragraph
        else:
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            formatted_lines.append(f'<p class="content-para">{stripped}</p>')
    
    # Close list if still open
    if in_list:
        formatted_lines.append('</ul>')
    
    result = '\n'.join(formatted_lines)
    
    return result

# Query Ollama API
def query_ollama(prompt):
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        if response.status_code == 200:
            raw_response = response.json().get('response', 'No response from model')
            # Format the response before returning
            return format_response(raw_response)
        else:
            return f"<p class='error-message'>Error: Unable to get response (Status: {response.status_code})</p>"
    except requests.exceptions.Timeout:
        return "<p class='error-message'>Error: Request timed out. Please try again.</p>"
    except requests.exceptions.ConnectionError:
        return "<p class='error-message'>Error: Cannot connect to Ollama server. Please ensure Ollama is running.</p>"
    except Exception as e:
        return f"<p class='error-message'>Error connecting to Ollama: {str(e)}</p>"

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('health_checker'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Check if user exists
                cursor.execute("SELECT id FROM users WHERE email = %s OR username = %s", (email, username))
                if cursor.fetchone():
                    flash('Username or email already exists!', 'danger')
                    return redirect(url_for('register'))
                
                # Insert new user
                hashed_pwd = hash_password(password)
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, hashed_pwd)
                )
                conn.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            if conn:
                conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not all([email, password]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('login'))
        
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                hashed_pwd = hash_password(password)
                cursor.execute(
                    "SELECT id, username, email FROM users WHERE email = %s AND password = %s",
                    (email, hashed_pwd)
                )
                user = cursor.fetchone()
                
                if user:
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['email'] = user['email']
                    flash('Login successful!', 'success')
                    return redirect(url_for('health_checker'))
                else:
                    flash('Invalid email or password!', 'danger')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            if conn:
                conn.close()
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT username, email, created_at FROM users WHERE id = %s", (session['user_id'],))
            user = cursor.fetchone()
            
            cursor.execute(
                "SELECT COUNT(*) as total FROM health_checks WHERE user_id = %s",
                (session['user_id'],)
            )
            stats = cursor.fetchone()
            
            return render_template('profile.html', user=user, stats=stats)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('health_checker'))
    finally:
        if conn:
            conn.close()

@app.route('/health-checker', methods=['GET', 'POST'])
@login_required
def health_checker():
    if request.method == 'POST':
        user_symptoms = request.form.get('symptoms')
        
        if not user_symptoms:
            flash('Please enter your symptoms!', 'warning')
            return redirect(url_for('health_checker'))
        
        # Enhanced prompt with medical information and tablet recommendations
        prompt = f"""You are a medical AI assistant. A user is experiencing the following symptoms: {user_symptoms}

Please provide a comprehensive response with:
1. Brief Analysis of the Symptoms
2. Possible Conditions (Not a Diagnosis)
3. General Recommendations and Medications/Tablets (if applicable)
4. When to Seek Medical Attention

Format your response clearly with numbered sections and bullet points where appropriate.
Remember: This is not a medical diagnosis. Always advise consulting a healthcare professional for proper diagnosis and treatment."""
        
        # Query Ollama
        response = query_ollama(prompt)
        
        # Save to database with formatted response
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Store user symptoms with the medical info prefix for context
                symptoms_with_context = f"Give the medical information and tablet. {user_symptoms}"
                cursor.execute(
                    "INSERT INTO health_checks (user_id, symptoms, ai_response) VALUES (%s, %s, %s)",
                    (session['user_id'], symptoms_with_context, response)
                )
                conn.commit()
                flash('Health check completed!', 'success')
        except Exception as e:
            flash(f'Error saving results: {str(e)}', 'danger')
        finally:
            if conn:
                conn.close()
        
        return render_template('health_checker.html', symptoms=user_symptoms, response=response)
    
    return render_template('health_checker.html')

@app.route('/history')
@login_required
def history():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, symptoms, ai_response, created_at FROM health_checks WHERE user_id = %s ORDER BY created_at DESC LIMIT 50",
                (session['user_id'],)
            )
            checks = cursor.fetchall()
            return render_template('history.html', checks=checks)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('health_checker'))
    finally:
        if conn:
            conn.close()

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)