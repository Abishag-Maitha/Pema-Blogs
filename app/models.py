from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(255), unique=True, nullable=False)
    email=db.Column(db.String(255), unique=True, index = True, nullable=False)

    password_secure=db.Column(db.String(255), nullable=False)
    bio=db.Column(db.String(255))
    profile_pic_path=db.Column(db.String())

    blogs=db.relationship("Blog",backref="user",lazy="dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
  
    @property
    def set_password(self):
        raise AttributeError("You cannot read the password attribute")

    @set_password.setter
    def password(self,password):
        self.password_secure=generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_secure,password)
    
    def save_u(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"User:{self.username}"


class Blog(db.Model):
    __tablename__="blogs"
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(255), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    time=db.Column(db.DateTime, default=datetime.utcnow)
    post=db.Column(db.Text(), nullable=False)
    comment = db.relationship('Comment',backref='blog',lazy='dynamic')
     
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"Blog:{self.post}" 


class Comment(db.Model):
    __tablename__="comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    comment = db.Column(db.Text(), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments=Comment.query.filter_by(blog_id=id).all()

        return comments

    def __repr__(self):
        return f"Comment{self.comment}"

class Subscriber(db.Model):
    __tablename__='subscribers'

    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True,index=True)

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Subscriber {self.email}'