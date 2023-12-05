from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from wtforms.validators import InputRequired, ValidationError, DataRequired, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_uploads import UploadSet, IMAGES, configure_uploads
from wtforms import StringField, PasswordField, SubmitField
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from datetime import datetime
import secrets
import os

app = Flask(__name__)


app.config['SECRET_KEY'] = 'Th1s I5 TcPCh472R00m'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:password@localhost/chatout" # login ke Mysql database #chatout bisa diganti database baru
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET'] = "XxxX"

db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
socketio = SocketIO(app, cors_allowed_origins="*")
socketio.init_app(app)

# login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):    
    return Users.query.get(int(id))

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads/photos')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#####################################################################
class Loginform(FlaskForm):
    email = StringField("Enter Your Email", validators=[DataRequired()])
    password = PasswordField("Enter Your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class Regform(FlaskForm):
    username = StringField("Enter Your Username", validators=[DataRequired()])
    email = StringField("Enter Your Email", validators=[DataRequired()])
    password = PasswordField("Enter Your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

#USERS
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    pictures = db.Column(db.String(100), nullable=False)
    SessionId = db.Column(db.String(50), unique=True, autoincrement=True)
    def __repr__(self):
        return '<User %r>' % self.username

# Dummy message document
class private_messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    reciever = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    save_at = db.Column(db.String(40), nullable=False)
    
# Dummy message document
class messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    SessionId = db.Column( db.String(50), unique=True, default="108fjo239joinhi41e0dr2hn")

# Creating rooms 
class Rooms(UserMixin, db.Model):
    room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_name = db.Column(db.String(50), nullable=False, unique=False)
    created_at = db.Column(db.String(40), nullable=False)

#
class Storing_messages(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_name = db.Column(db.String(50), nullable=False)
    room_name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    save_at = db.Column(db.String(20), nullable=False)


#####################################################################


def get_room(room_name):
    room_names = Rooms.query.filter_by(room_name=room_name).first()
    if room_names:
        return room_names
    else:
        return None


def updated_room(old_room_name, new_room_name):
    rooms = Rooms.query.filter_by(room_name=old_room_name).update({Rooms.room_name: new_room_name})
    if rooms:
        db.session.commit()
        return rooms
    else:
        return None



def update_session_id(username, sessionid):
    update = Users.query.filter_by(username=username).update({Users.SessionId: sessionid})
    if update:
        db.session.commit()
        return update
    else:
        return None


def return_only_username():
    return db.session.query(Users.username)


def save_messages(username, room_name, message):
    message = Storing_messages(sender_name=username, room_name=room_name, message=message, save_at=datetime.now())
    if message:
        db.session.add(message)
        db.session.commit()
        return message
    else:
        return None


def get_messages(room_name):
    return Storing_messages.query.filter_by(room_name=room_name)


def save_private_message(message, sender_name, reciever_name):
    message =  private_messages(message=message, sender=sender_name, reciever=reciever_name, save_at=datetime.now())
    if message:
        db.session.add(message)
        db.session.commit()
        return message
    else:
        return None
    
def get_private_message(sender_name, reciever_name):
    message = private_messages.query.filter_by(sender=sender_name, reciever=reciever_name).all()
    if message:
        return message
    else:
        return None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


#####################################################################

users= {}
@socketio.on('message')
def handle_message(message):
    print("Pesan : " + message)
    if message != "User connected!":
        send(message, broadcast=True)
        

# this is a private message socket
@socketio.on('private')
def private_message(msg):
    user_session = msg['usernames']
    message = msg['message']

    emit('new_private', message, room=user_session)

# private chat socket using session_ids
@socketio.on('username', namespace='/chat')
@login_required
def username(data):
    username = {'username': data}  # Mengubah string menjadi objek dictionary
    sessionid = Users.query.filter_by(username=username['username']).first()
    print(data)
    print(current_user.is_authenticated)
    if sessionid:
        update_session_id(sessionid.username, sessionid.SessionId)
        users[sessionid.username] = sessionid.SessionId
        print('username added')
        print(users)
        return sessionid

    
# sending the message to specific user
@socketio.on('private', namespace='/chat')
@login_required
def private(pyaload):
    username = Users.query.filter_by(username=pyaload['username']).first()
    if username:
        # users1 = list()
        recipient_session = users[pyaload['username']]
        print(users)  
        message = pyaload['message']
        now = datetime.now()
        time_stamp = now.strftime("%H:%M:%S")
        print(current_user.is_authenticated)
        if current_user.is_authenticated:
            save_private_message(message, current_user.username, pyaload['username'], time_stamp)
            emit('message', {"message": message, "username": current_user.email}, room=recipient_session)
            print(1234567890)
        else:
            print("Who are You  ")
    else:
        return "message not sent"
    

#####################################################################

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])   
def login(): 
    form = Loginform()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                user.is_authenticated = True
                flash('Login Successfully')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Password -- Try Again!')
        else:
            flash('User Not Found!..')
    return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Regform()
    name = None
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            photo = request.files['photo']
            if photo.filename == '':
                return 'Silahkan Masukkan Gambar Anda'
            if not allowed_file(photo.filename):
                return 'Format Gambar Tidak Sesuai'
            filename = secure_filename(photo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(filepath)
            
            password = bcrypt.generate_password_hash(form.password.data)
            user = Users(username=form.username.data, email=form.email.data, password=password,SessionId = secrets.token_urlsafe(32), pictures=filename)
            db.session.add(user)
            db.session.commit()
            
        name = form.username.data
        form.username.data = ''
        form.email.data = ''
        form.password.data = ''
        flash("Berhasil Ditambahkan")
        
        return redirect(url_for('login'))

    return render_template("register.html",form=form, name=name)

@app.route('/chat')
@login_required
def dashboard():
    alluser = Users.query.all()
    
    return render_template('dashchat.html', allusers=alluser)

@app.route('/chat/<username>', methods=['GET', 'POST'])
@login_required
def chatting(username):
    print(current_user.is_authenticated)
    alluser = Users.query.all()
    messages = get_private_message(current_user.username, username)
    print(messages, username)
    
    return render_template('dashchat.html', allusers=alluser, messages=messages, name=current_user.username)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    
    return redirect(url_for('login'),flash("Logout is Success.."))

#Error handling jika halaman tidak ditemukan
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    host = '127.0.0.1'
    app.run(debug=True, host=host)
