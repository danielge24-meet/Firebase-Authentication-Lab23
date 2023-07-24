from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

Config = {
  "apiKey": "AIzaSyAygQmd_ys9oQzq1DQJ_sCBFkpUXQrUdEc",
  "authDomain": "first-base-21881.firebaseapp.com",
  "projectId": "first-base-21881",
  "storageBucket": "first-base-21881.appspot.com",
  "messagingSenderId": "1072098846707",
  "appId": "1:1072098846707:web:eab3df6352c700e2f11486",
  "measurementId": "G-NL6VB7HXGJ",
  "databaseURL": "https://first-base-21881-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app (Config)
auth = firebase.auth()
db=firebase.database()


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            return redirect(url_for('signin'))
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        return redirect(url_for('add_tweet'))
       except Exception as e:
        print(e)
        return redirect(url_for('signup'))
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


if __name__ == '__main__':
    app.run(debug=True)