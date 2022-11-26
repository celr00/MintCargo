from flask_app import app, mysql
from flask import render_template, session, redirect, request

@app.route('/admin_users')
def users():
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login') 

    cursor = mysql.connection.cursor()

    cursor.execute('SELECT company_name, username, password FROM companies')
    users = cursor.fetchall()

    cursor.close()

    return render_template('users.html', users=users)