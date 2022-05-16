from flask_login import login_required,current_user
from flask import flash, render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Blog,Comment,Subscriber
from .forms import UpdateProfile, Makepost,Comment_Form
from ..requests import get_quotes
from .. import db #photos


@main.route('/') #, methods=['GET','POST'])
def index():
    title='Pema-Blogs'
    all_blogs=Blog.query.all()
    
    return render_template("index.html", blogs=all_blogs)

@main.route('/quotes')
def quotes():
    quotes = get_quotes()
    return render_template('quotes.html', quotes = quotes)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form =form)

@main.route('/new_blog', methods=['POST','GET'])
@login_required
def new_blog():
    subscribers = Subscriber.query.all()
    form = Makepost()
    if form.validate_on_submit():
        title = form.title.data
        user_id =  current_user._get_current_object().id
        blog = Blog(title=title,post=form.content.data, user_id=user_id)

        blog.save()
      
        return redirect(url_for('main.index'))
      
    return render_template('create_blog.html', form = form)
@main.route('/blog/<id>')
def blog(id):
    comments = Comment.query.filter_by(blog_id=id).all()
    blog = Blog.query.get(id)
    return render_template('index.html',blog=blog,comments=comments)


@main.route('/comment/<blog_id>', methods = ['Post','GET'])
@login_required
def comment(blog_id):
    form=Comment_Form()
    
    blog = Blog.query.get(blog_id)
    # comment =request.form.get('new_comment')
    user_id =  current_user._get_current_object().id
    if form.validate_on_submit():
        new_comment = Comment(comment=form.content.data, user_id=user_id,blog_id=blog_id)
        new_comment.save()
        return redirect(url_for('main.blog',id = blog.id))
    return render_template("new_comments.html",form=form)

@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))

@main.route('/blog/<blog_id>/delete', methods = ['POST','GET'])
@login_required
def delete_post(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    flash("You have deleted your Blog succesfully!")
    return redirect(url_for('main.index'))

