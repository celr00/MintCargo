from flask_app import app, mysql
from flask import render_template, session, redirect, request, url_for

@app.route('/admin_users')
@app.route('/admin_users/<msg>')
def users(msg=None):
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    cursor = mysql.connection.cursor()

    cursor.execute('SELECT company_name, username, password FROM companies')
    users = cursor.fetchall()

    cursor.close()

    if msg:
        return render_template('users.html', users=users, msg=msg)

    return render_template('users.html', users=users)

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
            return redirect(url_for('users', msg="Passwords don't match"))

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM companies WHERE username = %s', (_username,))
        unique = len(cursor.fetchall()) == 0

        if not unique:
            cursor.close()
            return redirect(url_for('users', msg="Username already exists"))

        print(_cName, _username, _pass)
        cursor.execute('INSERT INTO companies (company_name, username, password) VALUES (%s, %s, %s)', (_cName, _username, _pass,))

        mysql.connection.commit()
        cursor.close()
        return redirect('/admin_users')
        
@app.route('/update-customer', methods=['GET', 'POST'])
def updateCustomer():
    #Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    if request.method == 'POST':
        #Get user details
        _cName = request.form['company-name']
        _username = request.form['username']
        _pass = request.form['password']
        _id = int(request.form['id'])+1

        cursor = mysql.connection.cursor()

        #Checking is new username is not unique
        cursor.execute('SELECT * FROM companies WHERE company_id = %s', (_id,))

        current_info = cursor.fetchone()

        if _username != current_info[2]:
            cursor.execute('SELECT * FROM companies WHERE username = %s', (_username,))

            unique = len(cursor.fetchall()) == 0

            if not unique:
                cursor.close()
                return redirect(url_for('users', msg="Username already exists"+str(_id), operation='update'))

        cursor.execute('UPDATE companies SET company_name = %s, username = %s, password = %s WHERE company_id = %s', (_cName,_username, _pass, _id,))

        mysql.connection.commit()
        cursor.close()
        return redirect('/admin_users')
        
