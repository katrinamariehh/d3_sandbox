from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get('user_id'):
        return "User %s is logged in!" %session['user_id']
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    model.connect_to_db()
    username = request.form.get("username")
    password = request.form.get("password")

    user_id = model.authenticate(username, password)
    print user_id

    if user_id:
        flash("User authenticated")
        session['user_id'] = user_id
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!!!")

    return redirect(url_for("index"))

@app.route("/register")
def register():
    model.connect_to_db()
    return render_template("register.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/user/<username>')
def view_user(username):
    model.connect_to_db()
    user_id = model.get_user_by_name(username)
    wall_posts = model.get_wall_posts_for_user(user_id)

    return render_template("wall_posts.html", username = username,
                                              wall_posts = wall_posts,
                                              user_id = session.get('user_id'))

@app.route('/user/<username>', methods=["POST"])
def post_to_wall(username):
    model.connect_to_db()
    wall_owner = model.get_user_by_name(username)
    current_user = session.get('user_id')
    wall_content = request.form.get("wall_content")
    model.add_wall_post(current_user, wall_owner, wall_content)

    return redirect(url_for('view_user', username=username))

if __name__ == "__main__":
    app.run(debug = True)