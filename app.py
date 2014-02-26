from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get('username'):
        return "User %s is logged in!" %session['username']
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    if model.authenticate(username, password):
        flash("User authenticated")
        session['username'] = username
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!!!")

    return redirect(url_for("index"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug = True)
