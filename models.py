from flask_login import UserMixin
from ext import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel():
    def save(self):
        db.session.add(self)
        db.session.commit()  
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @staticmethod
    def update():
        db.session.commit()
        
       



class Service(db.Model, BaseModel):
    
    __tablename__ = "services"
    
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    details = db.Column(db.String())
    price = db.Column(db.Integer())
    img = db.Column(db.String(), nullable=True)
    imgurl=db.Column(db.String(), nullable=False)
    
class Course(db.Model, BaseModel):
    
    __tablename__ = "courses"
    
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    details = db.Column(db.String())
    price = db.Column(db.Integer())
    img = db.Column(db.String(), nullable=True)
    imgurl=db.Column(db.String(), nullable=False)
    
    
class Software(db.Model, BaseModel):
    
    __tablename__ = "softwares"
    
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    details = db.Column(db.String())
    price = db.Column(db.Integer())
    img = db.Column(db.String(), nullable=True)
    imgurl=db.Column(db.String(), nullable=False)
    
class Post(db.Model, BaseModel):
    
    __tablename__ = "posts"
    
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    subtitle = db.Column(db.String())
    description = db.Column(db.String())
    author = db.Column(db.String(), nullable=False)
    imgurl = db.Column(db.String(), nullable=False)
    likes = db.Column(db.Integer, default=0)
    liked_users = db.relationship('Like', backref='post', cascade='all, delete-orphan')
    
    
class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),
    )

      

    
    
class User(db.Model, BaseModel, UserMixin):
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    email = db.Column(db.String())
    name = db.Column(db.String())
    surname = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.String(), default="User")
    likes = db.relationship('Like', backref='user', cascade='all, delete-orphan')

    @property
    def liked_posts(self):
        return [like.post_id for like in self.likes]
    
    def __init__(self, username, email, name, surname, password, role="User"):
        self.username = username
        self.email = email
        self.name = name
        self.surname = surname
        self.password = generate_password_hash(password)
        self.role = role
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)