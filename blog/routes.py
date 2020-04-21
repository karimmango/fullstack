from flask import *
import secrets
import os
from PIL import Image
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
        db.session.add(user.follow(user))
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_pic = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.biography= form.biography.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.biography.data = current_user.biography
    profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    return render_template('account.html', title='Account',
                           profile_pic=profile_pic, form=form)

@app.route('/account/<username>', methods=['GET'])
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user.html', user=user)

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

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    if user == current_user.username:
        flash('You can\'t follow yourself!')
        return redirect(url_for('profile', username=username))
    u = current_user.follow(user)
    if u is None:
        flash('Cannot follow ' + username + '.')
        return redirect(url_for('profile', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + username + '!')
    return redirect(url_for('profile', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    if user == current_user.username:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', username=username))
    u = current_user.unfollow(username)
    if u is None:
        flash('Cannot unfollow ' + username + '.')
        return redirect(url_for('profile', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + username + '.')
    return redirect(url_for('user', username=username))

