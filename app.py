from flask import Flask, render_template,redirect,session
from models import db, connect_db, User, Feedback
from form import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask-feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "thissosecret"
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
db.create_all()

@app.route('/')
def get_home():
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register(): 
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)
        
        db.session.commit()
        session['username'] = user.username


        return redirect (f'/users/{username}')

    else:
        return render_template('/users/register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login(): 
    

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect (f'/users/{username}')

        else:
            form.username.errors = ["Invalid username/password."]
            return render_template('/users/login.html', form=form)   

    else:
        return render_template('/users/login.html', form=form)   


@app.route('/users/<username>')
def user_info(username):
    if "username" not in session or username != session['username']:
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        form = DeleteForm()
    
    return render_template("users/show.html", user=user, form=form)         

@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/login")

@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    if "username" not in session or username != session['username']:
        return redirect('/login')

    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
       
        feedback = Feedback(title=title,content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{username}')
    else:    
        return render_template("feedback/new.html", form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST']) 
def feedback_update(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        return redirect('/login')
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title= form.title.data
        feedback.content =form.content.data

        db.session.commit()
        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit.html", form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])   
def delete_feedback(feedback_id): 
    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        return redirect('/login')

    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")   



