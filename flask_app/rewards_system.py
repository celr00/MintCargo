from flask_app import app, mysql
from flask import render_template

@app.route('/rewards')
def rewards():

    cursor = mysql.connection.cursor()

    # Get product data
    cursor.execute('SELECT * FROM products')
    data = cursor.fetchall()
    cursor.close()

    return render_template('rewards.html', data=data)
