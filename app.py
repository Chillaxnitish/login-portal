import os
import json
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from JSON
def load_users():
    with open('users.json') as f:
        return json.load(f)

# Save submissions to JSON file
def save_submission(data):
    with open('submissions.json', 'r+') as f:
        submissions = json.load(f)
        submissions.append(data)
        f.seek(0)
        json.dump(submissions, f, indent=2)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            hashed = users[username]
            if check_password_hash(hashed, password):
                session['username'] = username
                return redirect(url_for('form'))
            else:
                error = 'Incorrect password.'
        else:
            error = 'User does not exist.'
    
    return render_template('login.html', error=error)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = {
            'username': session['username'],
            'field1': request.form['field1'],
            'field2': request.form['field2']
        }
        save_submission(data)
        return render_template('success.html', username=session['username'])
    
    return render_template('form.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
