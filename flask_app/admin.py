from flask_app import app, mysql
from flask import render_template, session, redirect, request

def getUsers():
    cursor = mysql.connection.cursor()

    cursor.execute('SELECT company_name, username, password FROM companies')
    users = cursor.fetchall()

    cursor.close()
    return users

@app.route('/admin_users')
def users():
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    return render_template('users.html', users=getUsers())

@app.route('/create-user', methods=['GET', 'POST'])
def addUser():
    #Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login') 

    if request.method == 'POST':
        #Get user details
        _cName = request.form['company-name']
        _username = request.form['username']
        _pass = request.form['password']
        _passC = request.form['password-conf']

        if _pass != _passC:
            return render_template('users.html', users=getUsers(), msg="Passwords do not match")

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM companies WHERE username = %s', (_username,))
        unique = len(cursor.fetchall()) == 0

        if not unique:
            cursor.close()
            return render_template('users.html', users=getUsers(), msg="Username already exists")

        print(_cName, _username, _pass)
        cursor.execute('INSERT INTO companies (company_name, username, password) VALUES (%s, %s, %s)', (_cName, _username, _pass,))

        mysql.connection.commit()
        cursor.close()
        return redirect('/admin_users')
        
