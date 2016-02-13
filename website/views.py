from flask import render_template, url_for, session, request, g, flash
from flask.ext.login import login_required, login_user, logout_user, current_user

from website.models import db, User, check_pass
from website.forms import Login, Register
from website import app


@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def login():
	l_form = Login(request.form, prefix="login-form")
	if l_form.validate_on_submit():
		try:
			user = User.get(User.username == l_form.username.data)
			check_login = check_pass(user.username, l_form.password.data)
		except:
			check_login = False
		if check_login == True:
		    session['username'] = user.username
		    return redirect(url_for('index'))
	return render_template('index.html', login=l_form, sign_up=Register())


@app.route('/register', methods=['POST'])
def register():
	r_form = Register(request.form, prefix="register-form")
	if r_form.validate_on_submit():
		try:
			User.create_user("barcai", "udvardy.zsombor@gmail.com", "cat", "0769696969", True)
			return redirect(url_for('index'))
		except:
			pass
	return render_template('index.html', login=Login(), sign_up=r_form)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('index'))