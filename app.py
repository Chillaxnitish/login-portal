import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    with open('users.json') as f:
        return json.load(f)

def save_submission(data):
    with open('submissions.json', 'r+') as f:
        submissions = json.load(f)
        submissions.append(data)
        f.seek(0)
        json.dump(submissions, f, indent=2)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('form'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

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
        return render_template('success.html')
    return render_template('form.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Dynamically use the port provided by Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
