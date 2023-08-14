'''
This is the site where users register and log in
'''

from flask import Flask, Response, abort, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin, current_user, login_required, login_user, logout_user
)

app = Flask(__name__)
app.config.update(DEBUG = True, SECRET_KEY="secret_key")

login_manager = LoginManager()
login_manager.init_app(app)

user_id = 1

users = [{"username":"test1", "password":"test1", "id": 1}, \
         {"username":"test2", "password":"test2", "id": 2}]
shopping_list = ["Green Tea Soy Latte", "Iced Mocha", "Iced Latte", "Pink Drink"]
comments = []

class User(UserMixin):
    ...


def get_user(user_id: int):
    for user in users:
        if int(user["id"]) == int(user_id):
            return user
    return None


@login_manager.user_loader
def user_loader(id: int):
    user = get_user(id)
    if user:
        user_model = User()
        user_model.id = user["id"]
        return user_model
    return None


@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        print(f"username = {username}, password = {password}, len = {len(users)}")

        for u in users:
            print(f"{u['username']}:{u['password']}")
            if u["username"] == username and u["password"] == password:
                user_model = User()
                user_model.id = u["id"]
                login_user(user_model)
                return redirect(url_for("shopping"))
            
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if len(username) > 0 and len(password) > 0:
            user_id+=1
            new_user = {"username":username, "password":password, "id": user_id}
            users.append(new_user)
            return redirect(url_for("/"))

    return render_template("register.html")


@app.route("/milktea-shop", methods=["GET", "POST"])
@login_required
def shopping():
    if request.method == "POST":
        new_comment = request.form.get('comment')
        link_url = request.form.get('link_url')
        link_text = request.form.get('link_text')

        if new_comment != None:
            comments.append([new_comment, link_url, link_text])
            return redirect(url_for("shopping"))
    else:
        print(f"GET method, total comments = {len(comments)}")
    return render_template("shopping_list.html", shopping_list = shopping_list, comments=comments )


@app.route("/logout")
@login_required
def log_out():
    logout_user()
    return redirect(url_for("homepage"))

if __name__ == "__main__":
    app.run(port=6678, debug=True)


# <!-- <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"> -->