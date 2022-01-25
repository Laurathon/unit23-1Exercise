"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug=DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return redirect("/users")
    #return render_template('list.html', users=users)

"""Show users main page"""    
@app.route('/users')
def users_index():  
    users = User.query.all()
    return render_template('users/index.html', users=users)

"""Show information on a certain user"""
@app.route('/<int:user_id>')
def users_show(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/show-user.html', user=user)

""" Edit an existing user"""
@ app.route('/<int:user_id>/edit')
def users_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit-user.html', user=user)


"""Update User information-submit form"""  
@app.route('/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")    

"""Add a new user, show form"""  
@app.route('/users/new', methods=["GET"])
def add_user(): 
    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    
    new_user  = User(first_name=first_name, last_name=last_name, image_url="http:\\test/test.jpg")
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

"""Deleting an existing user"""
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):   

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
