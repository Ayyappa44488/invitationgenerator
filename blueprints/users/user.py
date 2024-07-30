from flask import Blueprint, request, jsonify,redirect,render_template,session
from blueprints.users.models import User
from app import db

user=Blueprint('user',__name__,template_folder='templates')


@user.route('/login')
def login():
    return render_template('login.html')


@user.route('/register',methods=['POST'])
def register():
    name=request.form['name']
    email=request.form['email']
    password=request.form['password']

    data=User(name=name,email=email,password=password)

    db.session.add(data)
    db.session.commit()

    session['logged_in']=True
    session['user_id']=data.id
    session['user_name']=(data.name).capitalize()
    session['subscription']= "Free Plan"
    
    return redirect('/#pricing')


@user.route('/validate',methods=['POST'])
def validate():
    email=request.form['email']
    password=request.form['password']
    data=User.query.filter_by(email=email).first()

    if data and data.verify_password(password):
        session['logged_in']=True
        session['user_id']=data.id
        session['user_name']=(data.name).capitalize()
        session['subscription']= "Free Plan" if data.subscription==0 else "Premium Plan"
        return redirect('/')

    else:
        return jsonify({'message':'Login Failed'})

@user.route('/subscribe/<int:id>')
def subscribe(id):
    user=User.query.filter_by(id=session['user_id']).first()
    user.subscription=id
    db.session.commit()
    session['subscription']= "Free Plan" if user.subscription==0 else "Premium Plan"
    return redirect('/')

@user.route('/logout')
def logout():
    session.clear()

    return redirect('/')
