# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import sqlite3
from markupsafe import escape

# create the Flask app
from flask import Flask, render_template, request, session, redirect, flash
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///todo.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretKey'

# set up a 'model' for the data you want to store
from db_schema import db, Users, ListNames, ListItems, dbinit

# init the database so it can connect with our app
db.init_app(app)

from werkzeug import security
from flask_login import LoginManager, login_user, current_user, logout_user

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# select the database filename
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///todo.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# change this to False to avoid resetting the database every time this app is restarted
resetdb = True
if resetdb:
    with app.app_context():
        # drop everything, create all the tables, then put some data into the tables
        db.drop_all()
        db.create_all()
        dbinit()

@app.route('/')
def default():
    if current_user.is_authenticated:
        return redirect('/home2')
    else:
        return redirect('/home')

#route to the home
@app.route('/home')
def home():
    return render_template('home.html',page_title="To do list tool:")

#route to home2
@app.route('/home2')
def home2():
    return render_template('home2.html',page_title="To do list tool:", username=current_user.username, username_id = current_user.id )

#route to the login
@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first()

        if user is None:
            return redirect('/')
        if not security.check_password_hash(user.password_hash, password):
            return redirect('login')

        login_user(user)
        return redirect('/')

    return render_template('login.html',page_title="login:")

#route to the register
@app.route('/register', methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        password_hash=security.generate_password_hash(password)

        try:
            db.session.add(Users(username,password_hash))
            db.session.commit()
        except IntegrityError as exc:
            db.session.rollback()
            flash("Username Taken")
            return render_template('register.html',page_title="register:")

        user = Users.query.filter_by(username=username).first()
        login_user(user)
        return redirect('/')

    return render_template('register.html',page_title="register:")

#logout
@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged yourself out.')
    return redirect('/')

#route to the viewLists
@app.route('/viewLists')
def viewLists():
    if not current_user.is_authenticated:
        return redirect('/')

    user_id=current_user.id
    listNames = ListNames.query.filter_by(user_id=user_id).all()
    listItems = ListItems.query.all()
    return render_template('viewLists.html',page_title="viewLists:",listNames=listNames,listItems=listItems)

#route to the manageLists
@app.route('/manageLists')
def manageLists():
    if not current_user.is_authenticated:
        return redirect('/')

    return render_template('manageLists.html',page_title="manageLists:")

#route to the createNewList
@app.route('/createNewList',methods=['POST','GET'])
def createNewList():
    if not current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        newListName = request.form['newListName']

        if newListName!=None:
            db.session.add(ListNames(newListName,current_user.id))
            db.session.commit()
            return render_template('createNewList.html',page_title="createNewList:")
        else:
            return render_template('createNewList.html',page_title="createNewList:")
    return render_template('createNewList.html',page_title="createNewList:")
    
#route to the editList
@app.route('/editList',methods=['POST','GET'])
def editList():
    if not current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        listName = request.form['listName']
        itemName = request.form['itemName']

        listName = ListNames.query.filter_by(user_id=current_user.id,name=listName).first()

        if listName != None and listName.user_id == current_user.id:
            if itemName!=None:
                db.session.add(ListItems(itemName,"✗",listName.id))
                db.session.commit()
                return redirect('editList')

    return render_template('editList.html',page_title="editList:")


@app.route('/changeItem')
def changeItem():
    query = request.args.get('q').lower()
    queries = query.split()
    item = ListItems.query.filter_by(id=queries[1]).first()
    if (queries[0]=="✓"):
        item.completed_status="✓"
    else:
        item.completed_status="✗"
    
    db.session.commit()
    return ""


@app.route('/addItem',methods=['POST','GET'])
def addItem():

    if request.method == 'POST':
        listName = request.form['listName']
        itemName = request.form['itemName']

        listName = ListNames.query.filter_by(user_id=current_user.id,name=listName).first()

        if listName != None and listName.user_id == current_user.id:
            if itemName!=None:
                db.session.add(ListItems(itemName,"✗",listName.id))
                db.session.commit()
                return ""

    return ""
    