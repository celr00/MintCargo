from flask_app import app, mysql
from flask import render_template, session, redirect, request

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Delete credentials from session
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/')

@app.route('/pythonlogin', methods=['GET', 'POST'])
def pythonlogin():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Extract credentials
        _user = request.form['username']
        _pass = request.form['password']

        # Validate in MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s;', (_user, _pass,))
        account = cursor.fetchone()

        # Account exists in DB
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            return redirect('/')
        # Unknown credentials
        else:
            msg = 'Incorrect username or password'

    return render_template('login.html', msg=msg)