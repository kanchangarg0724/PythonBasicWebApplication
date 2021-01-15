from flask import Flask, render_template, redirect, url_for,  request, session

app = Flask(__name__)
app.secret_key = "12345"

@app.route('/')
def index():
    # Always redirect user to the login page
    if session['logged_in']:
        return redirect(url_for("user_profile"))
    else:
        return redirect(url_for("login_user"))


@app.route('/login', methods=['GET','POST'])
def login_user():

    if request.method == 'POST':
        loginfrm = request.form
        username = loginfrm['username']
        password = loginfrm['password']

        # Verify user from the text file
        if verify_user(username, password):
            session['logged_in'] = True
            return redirect(url_for("user_profile"))
        else:
            return "wrong password!"

    return render_template("login.html")


@app.route('/register', methods=['GET','POST'])
def new_user():

    if request.method == 'POST':
        loginfrm = request.form
        firstname = loginfrm['firstname']
        lastname = loginfrm['lastname']
        password = loginfrm['password']

        username = firstname[0:3] + lastname[0:3]

        # Verify user from the text file
        if add_user(username, password):
            session['logged_in'] = True
            return redirect(url_for("user_profile"))
        else:
            return "Try Again!"

    return render_template("register.html")


@app.route('/profile')
def user_profile():

    if session['logged_in']:
        return render_template("profile.html")
    else:
        return index()

@app.route('/logout')
def logout():
  session['logged_in'] = False
  return index()


def verify_user(username, password):

    # Opening the file "users.txt" in read mode
    file1 = open("users.txt", "r")

    result = False

    users = file1.read()

    user = users.split("\n")
    for userdetails in user:
        fileusername, filepassword = userdetails.split(" ")
        if (username == fileusername) and  (password == filepassword):
            result = True
            break

    # Closing a file
    file1.close()

    return result

def add_user(username, password):

    # Append new user details at the last of the file "users.txt"
    file1 = open("users.txt", "a")

    file1.write("\n"+username+" "+password)

    # Closing a file
    file1.close()

    return True

if __name__ == '__main__':
    app.run(debug=True)