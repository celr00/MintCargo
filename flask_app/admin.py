from flask_app import app, mysql
from flask import render_template, session, redirect, request, url_for

@app.route('/admin_users')
@app.route('/admin_users/<msg>')
def users(msg=None):
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
                return redirect(url_for('users', msg="Username already exists"+str(_id), operation='update'))

        cursor.execute('UPDATE companies SET company_name = %s, username = %s, password = %s WHERE company_id = %s', (_cName,_username, _pass, _id,))

        mysql.connection.commit()
        cursor.close()
        return redirect('/admin_users')
        
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

        return render_template('addresses.html', addresses=addresses)
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

        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE addresses SET address_line1 = %s, address_line2 = %s, city = %s, state = %s, country = %s, zip_code = %s WHERE company_id = %s', (_ad1, _ad2, _city, _state, _country, _zip, _id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('getAddresses', company_id=_id))

@app.route('/delete-address', methods=['GET', 'POST'])
def deleteAddress():
    # Confirm login
    if not session['loggedin'] or session['id'] != 1:
        return redirect('/login')
    
    if request.method == 'POST':
        _id = request.form['address-id2']

        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM addresses WHERE address_id = %s', (_id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('getAddresses', company_id=_id))

        