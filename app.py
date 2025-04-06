from flask import Flask, render_template, request, redirect, session, url_for
from blockchain import Blockchain, Block
import datetime
import json
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'
bc = Blockchain()

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)["users"]

@app.route('/')
def home():
    return render_template('index.html', logged_in='username' in session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/vote')
        else:
            return render_template('login.html', error="Sai tài khoản hoặc mật khẩu")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        otp_input = request.form.get('otp_input')
        if otp_input != session.get('otp'):
            return render_template('vote.html', step='otp', error='Sai mã OTP')
        voter_id = session['username']
        candidate = session['candidate']
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_block = Block(len(bc.chain), now, voter_id, candidate, bc.get_latest_block().hash)
        success = bc.add_block(new_block, voter_id)
        session.pop('otp', None)
        session.pop('candidate', None)
        return render_template('vote.html', success=success, step='done')
    elif request.method == 'GET' or 'candidate' not in session:
        return render_template('vote.html', step='form')
    return render_template('vote.html', step='otp')

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    candidate = request.form['candidate']
    session['candidate'] = candidate
    session['otp'] = str(random.randint(100000, 999999))
    return render_template('vote.html', step='otp', otp=session['otp'])

@app.route('/results')
def results():
    result_count = {}
    for block in bc.chain[1:]:
        result_count[block.vote] = result_count.get(block.vote, 0) + 1
    return render_template('result.html', results=result_count)

@app.route('/status')
def status():
    valid = bc.is_chain_valid()
    return render_template('status.html', valid=valid)

if __name__ == '__main__':
    app.run(debug=True)