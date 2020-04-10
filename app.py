from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from helpers import salting
from flask_bcrypt import Bcrypt
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://baf5f9532c112a:3706b1a5@eu-cdbr-west-02.cleardb.net/heroku_f500c00e9456035'#database link
engine = create_engine('mysql://baf5f9532c112a:3706b1a5@eu-cdbr-west-02.cleardb.net/heroku_f500c00e9456035')
connection= engine.raw_connection()
cursor= connection.cursor()
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)

class User(db.Model):
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
    if request.method=='POST':
        _username= request.form['username']
        _password= request.form['password']
        
        _password= salting(_password)
        #_password= bcrypt.generate_password_hash(_password)
        #_password=_password.decode('utf-8')
        user_query=User.query.filter(User.username==_username)
        user=user_query.first()
        ans=bcrypt.check_password_hash(user.password, _password )
        print(ans)
        
        print(user.password)
        if user and ans:
            session['logged_in'] = True
            return 'login succesful'
        else:
            return('wrong password!')
    return render_template('login.html')

    

if __name__=='__main__':
    app.secret_key='secret'
    app.run(debug=True)