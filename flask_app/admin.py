from flask_app import app, mysql
from flask import render_template, session, redirect, request, url_for

@app.route('/admin/users')
@app.route('/admin/users/<msg>')
def admin_users(msg=None):
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    cursor = mysql.connection.cursor()

    cursor.execute('SELECT * FROM companies')
    users = cursor.fetchall()

    cursor.close()

    if msg:
        return render_template('users.html', users=users, msg=msg)

    return render_template('users.html', users=users)

@app.route('/create-user', methods=['GET', 'POST'])
def create_user():
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
            return redirect(url_for('admin_users', msg='Passwords don\'t match'))

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM companies WHERE username = %s', (_username,))
        unique = len(cursor.fetchall()) == 0

        if not unique:
            cursor.close()
            return redirect(url_for('admin_users', msg='Username already exists'))

        print(_cName, _username, _pass)
        cursor.execute('INSERT INTO companies (company_name, username, password) VALUES (%s, %s, %s)', (_cName, _username, _pass,))

        mysql.connection.commit()
        cursor.close()
        return redirect('/admin/users')

@app.route('/update-customer', methods=['GET', 'POST'])
def update_customer():
    #Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    if request.method == 'POST':
        #Get user details
        _cName = request.form['company-name']
        _username = request.form['username']
        _pass = request.form['password']
        _id = int(request.form['id'])

        cursor = mysql.connection.cursor()

        #Checking is new username is not unique
        cursor.execute('SELECT * FROM companies WHERE company_id = %s', (_id,))

        current_info = cursor.fetchone()

        if _username != current_info[2]:
            cursor.execute('SELECT * FROM companies WHERE username = %s', (_username,))

            unique = len(cursor.fetchall()) == 0

            if not unique:
                cursor.close()
                return redirect(url_for('admin_users', msg='Username already exists'+str(_id), operation='update'))

        cursor.execute('UPDATE companies SET company_name = %s, username = %s, password = %s WHERE company_id = %s', (_cName,_username, _pass, _id,))

        mysql.connection.commit()
        cursor.close()
        return redirect('/admin/users')

@app.route('/admin/invoices')
@app.route('/admin/invoices/<msg>')
def admin_invoices(msg=None):

    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    # Get invoices
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT invoice_id, company_name, valid_from, valid_until, awarded_points, spent_points, points.company_id FROM points NATURAL JOIN companies;')
    invoices_data = cursor.fetchall()

    # Get companies
    cursor.execute('SELECT * FROM companies;')
    companies_data = cursor.fetchall()

    cursor.close()

    if msg:
        return render_template('invoices.html', invoices=invoices_data, companies=companies_data, msg=msg)

    return render_template('invoices.html', invoices=invoices_data, companies=companies_data)

@app.route('/create-invoice', methods=['GET', 'POST'])
def create_invoice():

    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login') 

    if request.method == 'POST':
        # Get invoice details
        _invoice = request.form['invoice']
        _company = request.form['company']
        _until = request.form['valid-until']
        _points = request.form['awarded-points']

        # Validate id
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM points WHERE invoice_id = %s;', ('invoice_id', _invoice))
        unique = len(cursor.fetchall()) == 0

        if not unique:
            cursor.close()
            return redirect(url_for('admin_invoices', msg='ID already exists'))

        # Create invoice
        cursor.execute('INSERT INTO points (invoice_id, company_id, valid_from, valid_until, awarded_points) VALUES (%s, %s, CURDATE(), %s, %s);', (_invoice, _company, _until, _points))
        mysql.connection.commit()
        cursor.close()

        return redirect('/admin/invoices')

@app.route('/update-invoice', methods=['GET', 'POST'])
def update_invoice():
    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    if request.method == 'POST':
        # Get invoice details
        _invoice = request.form['invoice']
        _company = request.form['company']
        _from = request.form['valid-from']
        _until = request.form['valid-until']
        _awarded = int(request.form['awarded-points'])
        _spent = int(request.form['spent-points'])

        # Update invoice
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE points SET company_id = %s, valid_from = %s, valid_until = %s, awarded_points = %s, spent_points = %s WHERE invoice_id = %s', (_company, _from, _until, _awarded, _spent, _invoice))
        mysql.connection.commit()

        cursor.close()

        return redirect('/admin/invoices')

@app.route('/addresses/<company_id>')
def getAddresses(company_id):
    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    if request.method == 'GET':
        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM addresses WHERE company_id = %s', (company_id,))

        addresses = cursor.fetchall()

        cursor.close()

        return render_template('addresses.html', addresses=addresses, company_id=company_id)
    return render_template('addresses.html')

@app.route('/update-address', methods=['GET', 'POST'])
def updateAddress():
    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    if request.method == 'POST':
        _id = request.form['address-id']
        _ad1 = request.form['address1']
        _ad2 = request.form['address2']
        _city = request.form['city']
        _state = request.form['state']
        _country = request.form['country']
        _zip = request.form['zip']
        c_id = request.form['c_id']

        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE addresses SET address_line1 = %s, address_line2 = %s, city = %s, state = %s, country = %s, zip_code = %s WHERE address_id = %s', (_ad1, _ad2, _city, _state, _country, _zip, _id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('getAddresses', company_id=c_id))

@app.route('/admin/products')
@app.route('/admin/products/<msg>')
def admin_products(msg=None):

    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    # Get products
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM products;')
    product_data = cursor.fetchall()

    cursor.close()

    if msg:
        return render_template('products.html', products=product_data, msg=msg)

    return render_template('products.html', products=product_data)

@app.route('/delete-invoice', methods=['GET', 'POST'])
def delete_invoice():
    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    if request.method == 'POST':
        # Get invoice id
        _invoice = request.form['invoice']

        # Delete invoice
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM points WHERE %s = %s;', ('invoice_id', str(_invoice)))
        mysql.connection.commit()

        cursor.close()

        return redirect('/admin/invoices')

@app.route('/create-product', methods=['GET', 'POST'])
def create_product():

    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login') 

    if request.method == 'POST':
        print(request.form)
        # Get product details
        _name = request.form['name']
        _desc = request.form['description']
        _route = request.form['route']
        _price = request.form['price']
        _active = 0
        if 'active' in request.form:
            _active = 1

        # Create product
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO products (product_name, product_description, image_route, product_unit_price, active) VALUES (%s, %s, %s, %s, %s);', (_name, _desc, _route, _price, _active))
        mysql.connection.commit()

        cursor.close()

        return redirect('/admin/products')

@app.route('/create-address', methods=['GET', 'POST'])
def createAddress():
    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    if request.method == 'POST':
        _ad1 = request.form['address1c']
        _ad2 = request.form['address2c']
        _city = request.form['cityc']
        _state = request.form['statec']
        _country = request.form['countryc']
        _zip = request.form['zipc']
        _company_id = request.form['company_id']

        cursor = mysql.connection.cursor()

        if _ad2:
            cursor.execute('INSERT INTO addresses (address_line1, address_line2, city, state, country, zip_code, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', (_ad1, _ad2, _city, _state, _country, _zip, _company_id,))
        else:
            cursor.execute('INSERT INTO addresses (address_line1, city, state, country, zip_code, company_id) VALUES (%s, %s, %s, %s, %s, %s)', (_ad1, _city, _state, _country, _zip, _company_id,))

        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('getAddresses', company_id=_company_id))

@app.route('/update-product', methods=['GET', 'POST'])
def update_product():
    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    if request.method == 'POST':        
        # Get invoice details
        _product = request.form['product']
        _name = request.form['name']
        _desc = request.form['description']
        _route = request.form['route']
        _price = request.form['price']
        _active = 0
        if 'active' in request.form:
            _active = 1

        # Update product
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE products SET product_name = %s, product_description = %s, image_route = %s, product_unit_price = %s, active = %s WHERE product_id = %s;', (_name, _desc, _route, _price, _active, _product))
        mysql.connection.commit()

        cursor.close()

        return redirect('/admin/products')

@app.route('/admin/orders')
@app.route('/admin/orders/<msg>')
def admin_orders(msg=None):

    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    # Get orders
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT order_id, company_name, address_line1, product_name, quantity, product_unit_price * quantity, created_at, status FROM orders NATURAL JOIN companies NATURAL JOIN addresses NATURAL JOIN products;')
    order_data = cursor.fetchall()

    cursor.close()

    if msg:
        return render_template('orders.html', orders=order_data, msg=msg)

    return render_template('orders.html', orders=order_data)

@app.route('/update-order', methods=['GET', 'POST'])
def update_order():
    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    if request.method == 'POST':
        # Get order details
        _order = request.form['order']
        _status = request.form['status']

        # Update order
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE orders SET status = %s WHERE order_id = %s;', (_status, _order))
        mysql.connection.commit()

        cursor.close()

        return redirect('/admin/orders')

@app.route('/delete-order', methods=['GET', 'POST'])
def delete_order():
    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')

    if request.method == 'POST':
        # Get order id
        _order = request.form['order']

        # Delete order
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM orders WHERE order_id = %s;' % _order)
        mysql.connection.commit()

        cursor.close()

        return redirect('/admin/orders')
        
