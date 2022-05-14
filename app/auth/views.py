from email.message import EmailMessage
from flask import render_template,redirect,url_for, flash,request
from flask_login import login_user,logout_user,login_required
from . import auth
from ..models import User
from .forms import LoginForm,RegistrationForm
from .. import db


@auth.route('/sign_up',methods = ["GET","POST"])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        EmailMessage("Welcome to Pema-Blogs","email/welcome_user",user.email,user=user)
        
        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/sign_up.html',registration_form = form)
    

@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
    if user is not None and user.verify_password(login_form.password.data):
        login_user(user,login_form.remember.data)
        return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "blogs login"
    return render_template('auth/login.html',login_form = login_form,title=title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))