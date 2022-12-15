from calendar import month
from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_sqlalchemy import SQLAlchemy
import hashlib
from flask_login import login_user, logout_user, LoginManager, login_required, current_user, UserMixin
import time
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '<write_secret_key_here>' #change secret key
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

today = datetime.today().date() #get date
print(today)

months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

dates = [(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             30, 31),
             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28),
             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             30, 31),
             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             30),
             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             30, 31),
             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             30),
             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             30, 31),
             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             30, 31),
             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             30),
             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             30, 31),
             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             30),
             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             30, 31)]

def unique(list1):
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
        	#if there is not the same element in list append it
            unique_list.append(x)

    return unique_list

#ORM
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
#ORM
class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    todos = db.Column(db.String(1000), nullable=True)
    subject = db.Column(db.String(100), nullable=False)

db.create_all()

#Home page
@app.route("/")
def index():
    return render_template('home.html', date=today)

@app.route("/home")
def home():
    title = "Home"
    return render_template('home.html', date=today, title=title)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Profile page
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    title = "Profile"
    name = current_user.username
    return render_template('profile.html', date=today, name=name, title=title)

#Todos page
@app.route("/todos", methods=['GET', 'POST'])
@login_required
def todos():
    title = "Todos"
    todo_list = []
    if request.method == 'POST':
        subject = request.form['subject']
        print("subject: "+subject+"test")
        if subject != None and subject != "":
            print(subject)
            todo = Todos(user_id=current_user.id, todos="", username=current_user.username, subject=subject)
            db.session.add(todo)
            db.session.commit()


    todos = Todos.query.filter_by(user_id=current_user.id).all()
    print(todos)

    return render_template('todos.html', date=today, len=len(todos), todos=todos, title=title)

#Todo detailed page
@app.route(f"/todos/<int:site_id>", methods=['GET', 'POST'])
@login_required
def details(site_id=None):
    title = "Todo"
    day_of_year = datetime.now().timetuple().tm_yday
    print(day_of_year)

    todo = Todos.query.filter_by(id=site_id).first()

    unique_list = []
    subject = ""

    add = str(request.form.get('check'))
    result = add + ' '
    if todo.todos == None:
        todo.todos = result
    else:
        todo.todos += result
    db.session.commit()
    print(todo.todos)

    checked = todo.todos.split(' ')
    for i in range(0,len(checked)):
        if checked[i].isdigit():
            checked[i] = int(checked[i])

    unique_list = unique(checked)
    subject = todo.subject

    print(unique_list)


    print(dates[0][0])
    return render_template('details.html', date=today, title=title, len=len(months), dates=dates, months=months, day=day_of_year, checked=unique_list, subject=subject, todo_id=site_id)


@app.route(f"/todosframe/<int:site_id>", methods=['GET', 'POST'])
@login_required
def details_frame(site_id=None):
    title = "Todo"
    day_of_year = datetime.now().timetuple().tm_yday
    print(day_of_year)

    todo = Todos.query.filter_by(id=site_id).first()

    unique_list = []
    subject = ""

    add = str(request.form.get('check'))
    result = add + ' '
    if todo.todos == None:
        todo.todos = result
    else:
        todo.todos += result
    db.session.commit()
    print(todo.todos)

    checked = todo.todos.split(' ')
    for i in range(0,len(checked)):
        if checked[i].isdigit():
            checked[i] = int(checked[i])

    unique_list = unique(checked)
    subject = todo.subject

    print(unique_list)

    print(dates[0][0])
    return render_template('details_frame.html', date=today, title=title, len=len(months), dates=dates, months=months, day=day_of_year, checked=unique_list, subject=subject, todo_id=site_id)


#Delete
@app.route("/delete/<int:site_id>", methods=['GET', 'POST'])
@login_required
def delete(site_id=None):
    if request.method == 'POST':
        todo_to_delete = Todos.query.filter_by(id=site_id).first()
        if current_user.id == todo_to_delete.user_id:
            db.session.delete(todo_to_delete)
            db.session.commit()
        return redirect(url_for('todos'))

#Login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    title = "Login"
    error = None
    success = None
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        if valid_login(username,password):
            user = User.query.filter_by(username=username).first()
            #return log_the_user_in(request.form['username'])
            login_user(user)
            return redirect('profile')
            #success = f"You are welcome {request.form['username']}"
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method was GET or the credentials were invalid
    return render_template('login.html', date=today, error=error, success=success, title=title)

#Logout
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('login')

#Register
@app.route("/register", methods=['GET', 'POST'])
def register():
    title = "Register"
    error=None
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = hashlib.md5(request.form['password'].encode()).hexdigest()
            email = request.form['email']

            if(username != "" and password != 'd41d8cd98f00b204e9800998ecf8427e' and email != ""):
                user = User(username=username, password=password, email=email)

                db.session.add(user)
                db.session.commit()
                return redirect('/login')
            else:
                error = 'All spaces must be filled'
        return render_template('/register.html', date=today, error=error, title=title)
    except Exception:
        error='Username or email address has been used before!'
        return render_template('/register.html', date=today, error=error, title=title)


def valid_login(username, password):
    try:
        if (User.query.filter_by(username=username).first().username == username and User.query.filter_by(
                username=username).first().password == password):
            return 1
        else:
            return 0
    except AttributeError:
        return 0

if __name__ == '__main__':
   app.run()
