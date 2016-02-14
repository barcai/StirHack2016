import json
import sqlite3

from flask import redirect, render_template, url_for, session, request, g, flash
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
	if current_user.is_authenticated:
		return render_template("user.html")
	return render_template("index.html", login=Login(), sign_up=Register())


@app.route('/login', methods=['POST'])
def login():
	l_form = Login(request.form)
	if l_form.validate_on_submit():
		check_login = True
		try:
			user = User.get(User.username == l_form.username.data)
			check_login = check_pass(user.username, l_form.password.data)
		except:
			check_login = False
		if check_login == True:
			login_user(user)
			return redirect(url_for('user'))
	return render_template('index.html', login=l_form, sign_up=Register())


@app.route('/register', methods=['POST'])
def register():
	r_form = Register(request.form)
	if r_form.validate_on_submit():
		try:
			User.create_user(
				r_form.username.data, 
				r_form.email.data,
				r_form.password.data,
				r_form.phone_num.data)
			login_user(User.get(User.username == r_form.username.data))
			return render_template('index.html', login=l_form, sign_up=Register())
		except:
			l.error("Fuck THis shit")
	return render_template('index.html', login=Login(), sign_up=r_form)


@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash('You were logged out')
	return redirect(url_for('index'))


@app.route("/you")
@login_required
def user():
	conn = sqlite3.connect("old_saved.db")
	cursor = conn.execute("SELECT date, diag from Diagnostic Order by date DESC Limit 100;")
	dataset = crunching_dat_data(cursor)
	conn.close()
	return render_template("user.html", dataset = dataset)


def crunching_dat_data(dataset):
	ret = {'api8':0, 'api1':0, 'api7':0, 'api6':0, 'api3':0, 'api5':0, 'api4':0, 'api2':0}
	for data in dataset:
		s = dict(json.loads(json.loads(data[1])))
		print(type(s))
		for key in s.keys():
			if s[key]["message"] != "OK":
				ret[key] = ret[key] + 1
	print(ret)
	return json.dumps(ret)