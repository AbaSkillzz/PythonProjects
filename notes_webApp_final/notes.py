from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from sqlalchemy.orm import backref, defaultload
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, TextField
from wtforms import validators 
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash



#-------------------------------------------  APP CONFIGURATION ------------------------------------------------------------------
app = Flask(__name__)

app.config["SECRET_KEY"] = "qualcosaacaso"  #serve per criptare i vari dati sul server(protezione)

bootstrap = Bootstrap(app)


#/////////////////////////////////////////////// DATABASE ///////////////////////////////////////////////////////////////////
db_name = "PERCORSO_DATABASE" 
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class User(db.Model):  #creo una table(insieme di dati organizzati in una griglia)
    __tablename__  = "users"
    #cose che di cui ha bisogno della classe User(che ha bisogno ogni user)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=True)
    notes_created = db.relationship("Note", backref="author") 


class Note(db.Model):
    __tablename__ = "notes"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text()) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    
    

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ WEBSITE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#HOME PAGE
@app.route("/") 
def home():
    return render_template("home.html")
    

#USER'S PAGE
@app.route("/profile")
def profile():
    return render_template("profile.html")

#USER'S subdomain pages

class NewNote(FlaskForm):
    title = TextField("Your note's title: ", validators=[DataRequired()])
    note = TextAreaField("Write your note...", render_kw={"rows": 20, "cols": 140}, validators=[DataRequired()])
    submit = SubmitField("Save")

@app.route("/profile/newnote", methods=["GET", "POST"])
def newNote():
    note = NewNote()

    if request.method == "GET":
        return render_template("newnote.html", note_area=note)
    
    elif request.method == "POST":
        title = request.form["title"]
        data = request.form["note"]
        user = session["user"] #cerco l'attuale user della sessione in corso
        check_user = User.query.filter_by(username=user).first() 
        user_id = check_user.id

        note = Note(user_id=user_id, title=title, content=data)
        db.session.add(note)
        db.session.commit()
        flash("Successfully created your note!")

        return render_template("profile.html")



@app.route("/profile/opennotes", methods=["GET", "POST"])
def openNotes():
    user = session["user"]
    check_user = User.query.filter_by(username=user).first()
    check_user_id = check_user.id
    notes = Note.query.filter_by(user_id=check_user_id).all() #tutte le note relative all'id dell'attuale utente
    
    return render_template("opennotes.html", notes=notes)



#LOG-IN 
class LogIn(FlaskForm):
    username = StringField("Enter your username", validators=[DataRequired()])
    password = PasswordField("Enter the password", validators=[DataRequired()])
    submit = SubmitField("GO")

@app.route("/login", methods=["GET", "POST"]) #GET per aprire la pagina, POST per fare una richiesta al server con dati(le credenziali) 
def login():
    form = LogIn()

    if request.method == "GET":
        return render_template("login.html", form=form)

    elif request.method == "POST":
        username = request.form["username"]  #prendo username e password dal form
        password = request.form["password"]
        
        check_username = User.query.filter_by(username=username).first()  #filtro la table per cercare lo username 

        if check_username: #se è gia registrato
            if check_password_hash(check_username.password, password): #la funzione da True se la password combacia, False se non combaciano
                session["logged_in"] = True
                session["user"] = username
                return redirect(url_for('profile'))

            else:
                flash("INCORRECT PASSSWORD FOR THE GIVEN USERNAME")
                return render_template("login.html", form=form)
                

        else:  #se non esiste quello username
            flash("NO USERNAME FOUND, GO TO REGISTER IF YOU WANT TO CREATE ONE")
            return redirect(url_for('login'))
    
    

#SIGN-UP
class SignUp(FlaskForm): 
    username = StringField("Enter a nickanme", validators=[DataRequired()])
    password = PasswordField("Choose a password", validators=[DataRequired()])
    submit = SubmitField("SUBMIT")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUp()

    #solo per aprire la pagina
    if request.method == "GET":
        return render_template("signup.html", form=form)

    #se si vuole fare la registrazione
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password, method="sha256", salt_length=8)

        #controllo se username è stato gia preso
        check_username = User.query.filter_by(username=username).first()  #filtro la table User per username, e vedo se c'è lo username messo dallo user

        if check_username:
            flash("CHANGE USERNAME, ALREADY TAKEN")
            return redirect("signup")

        else:
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect("login")
        

@app.route("/logout")
def logout():
    session["logged_in"] = False
    session.pop("user", None)  #cancello lo username dell'utente che è savato in session["user"]
    return render_template("logout.html")


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



if __name__ == "__main__":

    #db.drop_all()
    db.create_all() #crea ogni modello(table) del database che si crea
    app.run(debug=True)

#--------------------------------------------------------------------------------------------------------------------------