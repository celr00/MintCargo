from flask_app import app, mysql
from flask import render_template, redirect, session, request

@app.route('/rewards')
def rewards():

    # Confirm login
    if not session.get('loggedin') or not session['loggedin']:
        return redirect('/login')

    cursor = mysql.connection.cursor()

    # Get product data
    cursor.execute('SELECT * FROM products')
    product_data = cursor.fetchall()

    # Get orders data
    cursor.execute('SELECT created_at, address_line1, SUM(points_spent), status FROM orders NATURAL JOIN order_details NATURAL JOIN addresses WHERE orders.company_id = %s GROUP BY orders.order_id ORDER BY created_at DESC;' % session['id'])
    orders_data = cursor.fetchall()

    # Get addresses data
    cursor.execute('SELECT * FROM addresses WHERE company_id = %s;' % session['id'])
    addresses_data = cursor.fetchall()

    cursor.close()

    return render_template('rewards.html', products=product_data, orders=orders_data, addresses=addresses_data)

@app.route('/update-user', methods=['GET', 'POST'])
def update_user():

    # Confirm login
    if not session.get('loggedin') or not session['loggedin']:
        return redirect('/login')

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Extract credentials
        _user = request.form['username']
        _pass = request.form['password']

        # Update credentials
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE companies SET username = %s, password = %s WHERE company_id = %s;', (_user, _pass, session['id']))
        mysql.connection.commit()
        session['user'] = _user
        
        cursor.close()

    return redirect('/rewards')