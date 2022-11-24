from flask_app import app, mysql
from flask import render_template, redirect, session

@app.route('/rewards')
def rewards():

    # Confirm login
    if not session.get('loggedin') or not session['loggedin']:
        return redirect('/login')

    cursor = mysql.connection.cursor()

    # Get product data
    cursor.execute('SELECT * FROM products')
    data = cursor.fetchall()
    cursor.close()

    return render_template('rewards.html', data=data)
