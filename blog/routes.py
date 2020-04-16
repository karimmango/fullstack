from flask import *
from blog.models import User, Post
from blog import app, bcrypt, db   
from blog.helpers import salting

from flask_login import login_user, current_user, logout_user, login_required
from blog.forms import RegForm, LoginForm, UpdateAccountForm, PostForm

@app.route('/')
@app.route('/home')
def index():
    posts= Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegForm()
    if form.validate_on_submit():
        salted_pass= salting(form.password.data)
        hashed_pass= bcrypt.generate_password_hash(salted_pass)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template("reg.html", title='Register an Account', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        passw=salting(form.password.data)
        if user and bcrypt.check_password_hash(user.password, passw ):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login Page', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('login')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    #image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def make_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('make_post.html', title='New Post', form=form )

@app.route('/post/<int:post_id>')
def post(post_id):
    post= Post.query.get_or_404(post_id)
    return render_template('posts.html', title=post.title, post=post)

