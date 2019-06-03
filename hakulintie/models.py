from datetime import datetime
from hakulintie import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

user_roles = db.Table('roles',
                db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
                db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                )

# Creating the user and post table models
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    house = db.Column(db.String(3), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Posts', backref='author', lazy=True)
    roles = db.relationship('Role',
                            secondary=user_roles,
                            backref=db.backref('users'), lazy='dynamic'
                            )

    # Method for checking if the user has certain roles
    def has_role(self, name):
        for role in self.roles:
            if role.name == name:
                return True
            return False

    def __repr__(self):
        return f'User <{self.email} | {self.first_name} | {self.last_name} | {self.house}>'

# Announcement posts model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'Post <{self.title} | {self.date_posted}>'

# User roles model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'Role <{self.name} | {self.description}>'