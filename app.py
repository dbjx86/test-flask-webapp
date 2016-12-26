from flask import Flask, render_template, redirect, request, url_for, session, flash

from flaskext.mysql import MySQL

from functools import wraps

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def login_requred(fn):
    @wraps(fn)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return fn(*args, **kwargs)
        else:
            flash("you need to login first")
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_requred
def home():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select name, email from users;")
    data = [dict(name=row[0], email=row[1]) for row in cursor.fetchall()]
    return render_template("index.html", data=data)

@app.route('/welcome')
@login_requred
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invaild credentials. Please try aagin'
        else:
            session['logged_in'] = True
            flash('you are logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_requred
def logout():
    session.pop('logged_in', None)
    flash('you are logged out!')
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.secret_key = 'plus 1 s'
    app.run(debug=True)
