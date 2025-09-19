from typing import Optional
from flask import Flask, render_template, redirect, flash
from forms import LoginForm, SignupForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlalchemy as sa
import sqlalchemy.orm as so

app = Flask(__name__)

app.config.from_object('default_config')
app.config.from_prefixed_env()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    def __repr__(self) -> str:
        return f"<User {self.username}>"

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    content: so.Mapped[str] = so.mapped_column(sa.String(512))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self) -> str:
        return f"<post {self.content}>"

@app.route('/')
def index_ep():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_ep():
    form = LoginForm()

    if form.validate_on_submit():
        flash('You are logged in.')
        return redirect('/')

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup_ep():
    form = SignupForm()

    if form.validate_on_submit():
        flash('You are now signed up.')
        return redirect('/')

    return render_template('signup.html', form=form)
