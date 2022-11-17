from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('privacy')
def privacy():
    return render_template('privacy.html')
    
@app.route('/about')
def about():
    return render_template('about-us.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy_policy():
    

if __name__ == '__main__':
    app.run(debug=True)
