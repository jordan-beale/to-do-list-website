from flask_sqlalchemy import SQLAlchemy

# create the database interface
db = SQLAlchemy()

# a model of a user for the database
class Base(db.Model):
    __tablename__='base'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20), unique=True)

    def __init__(self, username, password):  
        self.username=username
        self.password=password

# a model of a list for the database
# it refers to a user
class ListNames(db.Model):
    __tablename__='list_names'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    user_id = db.Column(db.Integer)  # this ought to be a "foreign key"

    def __init__(self, name, user_id):
        self.name=name
        self.user_id = user_id

# a model of a list item for the database
# it refers to a list
class ListItem(db.Model):
    __tablename__='list_elements'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    completedStatus = db.Column(db.Text())
    list_id = db.Column(db.Integer)  # this ought to be a "foreign key"

    def __init__(self, name, completedStatus, list_id):
        self.name=name
        self.completedStatus=completedStatus
        self.list_id=list_id

# put some data into the tables
def dbinit():
    user_list = [
        Base("Jordan","123"), 
        Base("Jack","abc"),
        Base("Jacob","petName")
        ]
    db.session.add_all(user_list)

    # find the id of the user Jordan
    jordan_id = Base.query.filter_by(username="Jordan").first().id

    all_lists = [
        ListNames("generalTasks",jordan_id), 
        ListNames("workTasks",jordan_id)
        ]
    db.session.add_all(all_lists)

    # find the ids of the lists Chores and Shopping

    generalTasks_id = ListNames.query.filter_by(name="generalTasks").first().id
    workTasks_id = ListNames.query.filter_by(name="workTasks").first().id

    all_items = [
        ListItem("clean room","complete",generalTasks_id), 
        ListItem("shower","incomplete",generalTasks_id),
        ListItem("do 141 coursework","complete",workTasks_id), 
        ListItem("finish 139 lab3","incomplete",workTasks_id)
        ]
    db.session.add_all(all_items)

    # commit all the changes to the database file
    db.session.commit()


# choose one to use for complete ✓ ✗ | use ☐ for incomplete