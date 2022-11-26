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
    cursor.execute('SELECT product_name, quantity, created_at, status FROM orders NATURAL JOIN products WHERE company_id = %s ORDER BY created_at DESC;' % session['id'])
    orders_data = cursor.fetchall()

    # Get addresses data
    cursor.execute('SELECT * FROM addresses WHERE company_id = %s;' % session['id'])
    addresses_data = cursor.fetchall()

    cursor.close()

    return render_template('rewards.html', products=product_data, orders=orders_data, addresses=addresses_data)

@app.route('/create-order', methods=['GET', 'POST'])
def create_order():

    # Confirm login
    if not session.get('loggedin') or not session['loggedin']:
        return redirect('/login')

    if request.method == 'POST' and 'quantity' in request.form:
        # Get order details
        _quantity = request.form['quantity']
        _product = request.form['product']

        # Save order
        cursor = mysql.connection.cursor()
        cursor.callproc('Orders_CreateOrder', (session['id'], _product, _quantity))
        points = cursor.fetchone()

        # Open and close cursor to commit changes to DB
        cursor.close()
        cursor = mysql.connection.cursor()
        mysql.connection.commit()

        # Subtract points
        session['points'] = points[0]

        cursor.close()
    
    return redirect('/rewards')

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
