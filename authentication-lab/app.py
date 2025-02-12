from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyDP30m2q17oFkngBiMOygMwZNMtFMCu6Ak",
  "authDomain": "firelab-5438d.firebaseapp.com",
  "projectId": "firelab-5438d",
  "storageBucket": "firelab-5438d.appspot.com",
  "messagingSenderId": "345681661251",
  "appId": "1:345681661251:web:224f5d12b310a37e25f3f6",
  "measurementId": "G-ZZXEY8J1BR", 
  "databaseURL" : "https://firelab-5438d-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():

    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        users = {"email" : request.form['email'], "password" : request.form['password'], "name" : request.form['name'], "username" : request.form['username'], "bio" : request.form['bio']}
        db.child("users").child(login_session['user']['localId']).set(users)
        try:
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
        return render_template("signup.html",error=error)
    return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        tweet = {"title" : request.form['title'], "text" : request.form['text'], "uid" : login_session['user']['localId']}
        db.child("tweet").push(tweet)
    return render_template("add_tweet.html")

@app.route("/all_tweets")
def all_tweets():
    tweets =db.child("tweet").get().val()
    return render_template("tweets.html", tweets = tweets)


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))
 


if __name__ == '__main__':
    app.run(debug=True)