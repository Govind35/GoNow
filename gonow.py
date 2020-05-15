from flask import Flask, render_template, url_for, flash, redirect, session
from flask_pymongo import PyMongo
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['MONGO_URI']="mongodb://localhost:27017/GoNow"
app.config['SECRET_KEY'] = '1q2w3e4r5t6y7u8i9o0p'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    print(session['username'])
    if 'username' in session:
        return render_template('home.html',posts = posts, user = session['username'])
    return render_template('home.html',posts = posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if mongo.db.user.find_one({'Username': form.username.data}):
            flash('Username is already taken !', 'danger')
        else:
            hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            mongo.db.user.insert_one({'Username' :form.username.data,'Email' :form.email.data, 'password' : hashed_pwd})
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html',title ='Registeration', form =form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm() 
    if form.validate_on_submit():
        user = mongo.db.user.find_one({'Username': form.username.data})
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            flash('You have been logged in!', 'success')
            session['username'] = form.username.data
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
