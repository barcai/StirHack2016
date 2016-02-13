from flask import render_template

from app import *
from models import check_pass


@app.before_request
def before_request():
    g.db = database
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.j2")


@app.route('/login', , methods=['POST'])
def index():
    l_form = Login(request.form, prefix="login-form")
    if l_form.validate():
    	try:
    		user = User.get(User.username == l_form.username.data)
    		check_login = check_pass(user.username, l_form.password.data)
    	except:
    		check_login = False
        if check_login == True:
            conn.commit()
            return redirect(url_for('me'))
    return render_template('index.j2', login=l_form, sign_up=Register())


@app.route('/register', methods=['POST'])
def register():
    r_form = Register(request.form, prefix="register-form")
    if r_form.validate():
        check_reg = cursor.execute("SELECT * FROM users WHERE username = '%s' OR `e-mail` = '%s'"
            % (r_form.username.data, r_form.email.data))

        if check_reg == False:
            cursor.execute("INSERT into users (username, pwd, `e-mail`) VALUES ('%s','%s','%s')"
                % (r_form.username.data, hashlib.sha1(r_form.password.data).hexdigest(), check_email(r_form.email.data)))
            conn.commit()
            return redirect(url_for('index'))
    return render_template('index.html', login=Login(), sign_up=r_form)



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
