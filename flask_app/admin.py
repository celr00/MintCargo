from flask_app import app, mysql
from flask import render_template, session, redirect, request

@app.route('/admin_users')
def users():
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login') 

    return render_template('users.html')