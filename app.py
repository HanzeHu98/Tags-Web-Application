from flask import (flash, redirect, render_template,
    request, session, url_for, Flask)
from data_persistence import *
import auth
from uuid import uuid4

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid4())

@app.route('/login', methods=['GET', 'POST'])
def login():
    # login code goes here
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get('password')

    authenticated = auth.authenticate(username, password)

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not authenticated:
        flash('Please check your login details and try again')
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page
    
    session['logged_in'] = True
    session['username'] = username
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session['logged_in'] = False
	return home()


@app.route('/')
@app.route('/home', methods=['GET', 'POST', "PUT", "DELETE"])
def home():
    """
    Go to login if not logged in, otherwise go to main page
    """
    if not session.get('logged_in'):
        return login()
    return render_template("list_tags.html", tags = db_fetch_tags(session['username']))

@app.route('/edit_tag', methods=['POST'])
def edit():
    if not session.get('logged_in'):
        return login()
    old_tag = request.form["old_tag"]
    new_tag = request.form["new_tag"]
    if db_update_tag(session['username'], old_tag, new_tag):
        return internal_error()
    return redirect(url_for("home"))

@app.route('/add_tag', methods=['POST'])
def create():
    if not session.get('logged_in'):
        return login()
    new_tag = request.form["new_tag"]
    if db_insert_tag(session['username'], new_tag):
        return internal_error()
    return redirect(url_for("home"))

@app.route('/delete_tag', methods=['POST'])
def delete():
    if not session.get('logged_in'):
        return login()
    tag = request.form["tag"]
    if db_delete_tag(session['username'], tag):
        return internal_error()
    return redirect(url_for("home"))

##-------------------------- ERROR HANDLER -----------------------------##

"""404 error handler
"""
@app.errorhandler(404)
def page_not_found(e):
  return render_template('error.html', 
    title='Page not found', alert_level='warning',
    message="The page you tried to reach does not exist. \
      Please check the URL and try again."
    ), 404

"""403 error handler
"""
@app.errorhandler(403)
def forbidden(e):
  return render_template('error.html',
    title='Not authorized', alert_level='danger',
    message="You are not authorized to access this page. \
      If you think you deserve to be granted access, please contact the \
      supreme leader of the mutating genome revolutionary party."
    ), 403

"""500 error handler
"""
@app.errorhandler(500)
def internal_error(error):
  return render_template('error.html',
    title='Server error', alert_level='danger',
    message="The server encountered an error and could \
      not process your request."
    ), 500



app.run(host='0.0.0.0', debug=True)