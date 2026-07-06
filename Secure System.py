import bcrypt
import random
from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


messages = [
    "Access Granted. Welcome back, Agent. 🔐",
    "Authentication successful. Stay secure. 🛡️",
    "Identity verified. Welcome back. 🚀",
    "System online. User authenticated successfully. 💻",
    "Welcome back. Stay curious and keep hacking ethically. 🐍",
    "Security first. Progress second. Success follows. 🔥",
    "Credentials verified. Mission accepted. 🎯",
    "Login successful. Remember: strong passwords save lives. 🔑",
    "Welcome back. One line of code at a time. 💡",
    "User recognized. Continue building greatness. ⭐"
]


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password = request.form["password"]

    # Validate username and password
    if len(username) < 5:
        return "Username must be at least 5 characters long."
    if len(password) < 12:
        return "Password must be at least 12 characters long."
    if password.isalpha():
        return "Password must contain at least one number."
    if password.isdigit():
        return "Password must contain at least one letter."
    if password.isalnum():
        return "Password must contain at least one special character."
    if password.islower():
        return "Password must contain at least one uppercase letter."
    if password.isupper():
        return "Password must contain at least one lowercase letter."

    # Hash the password
    encoded_password = password.encode()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(encoded_password, salt)

    # Save username and hashed password to file
    with open("data.txt", "a") as file:
        file.write(f"{username},{hashed_password.decode()}\n")

    return "Registration successful! You can now log in."


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")
    login_name = request.form["username"]
    login_pass = request.form["password"]

    authentic = False
    stored_hash = None

    with open("data.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")

            if login_name == data[0]:
                authentic = True
                stored_hash = data[1].strip().encode()
                break
        if not authentic:
            return "Please enter the correct username."
        if stored_hash is None:
            return "Username not found. Please try again."
        encoded_pass = login_pass.encode()

        if bcrypt.checkpw(encoded_pass, stored_hash):
            return render_template("dashboard.html", login_name=login_name, 
                                   message=random.choice(messages))
        else:
            return "Incorrect password. Please try again!"


@app.route("/password", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("password.html")

    with open("data.txt", "r") as file:
        data = file.read().splitlines()
        for line in data:
            line = line.strip().split(",")
            username = line[0].strip()
            password_hash = line[1].strip()
            with open("dictionary.txt", "r") as file:
                dictionary = file.read().splitlines()

            for word in dictionary:
                encoded_word = word.encode()
                if bcrypt.checkpw(encoded_word, password_hash.encode()):
                    return f"Password for {username} is weak and can be found in the dictionary."
    return "Your password is strong and not found in the common passwords" \
           " dictionary."


if __name__ == "__main__":
    app.run(debug=True)
