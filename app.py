from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from helpers import salting
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, LoginManager, UserMixin, logout_user

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://baf5f9532c112a:3706b1a5@eu-cdbr-west-02.cleardb.net/heroku_f500c00e9456035'#database link
engine = create_engine('mysql://baf5f9532c112a:3706b1a5@eu-cdbr-west-02.cleardb.net/heroku_f500c00e9456035')
connection= engine.raw_connection()
cursor= connection.cursor()
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manage= LoginManager(app)
@login_manage.user_loader
def load_user(id):
    return User.query.get(int(id))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(100), nullable=False, unique=True)
    email= db.Column(db.String(120), nullable=False, unique=False)
    password= db.Column(db.String(120), nullable=False)
 
db.create_all()
@app.route('/', methods=['GET'])
def index():
    
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    if request.method=='POST':
        _username= request.form['username']
        _email= request.form['email']
        _password= request.form['password']
        
        salted_pass= salting(_password)
        hashed_pass= bcrypt.generate_password_hash(salted_pass)
        try:
            db.session.add(User(username=_username,
            email=_email,
            password=hashed_pass))
            db.session.commit()
        except:
            print('error creating account')
            
        return redirect('/')
    return render_template("reg.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    if request.method=='POST':
        _username= request.form['username']
        _password= request.form['password']
        
        _password= salting(_password)
        user_query=User.query.filter(User.username==_username)
        user=user_query.first()
        ans=bcrypt.check_password_hash(user.password, _password )
        if user and ans:
            session['logged_in'] = True
            login_user(user)
            return redirect('account')
        else:
            flash('Login Unsuccessful!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('login')

@app.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('index.html')



if __name__=='__main__':
    app.secret_key='secret'
    app.run(debug=True)