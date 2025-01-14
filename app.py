from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from flask import session, redirect, url_for
from flask import flash
from datetime import timedelta
from SQL.db import DB
import tensorflow as tf
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

dataset = pd.read_csv("dataset.csv")

vectorizer = CountVectorizer()
vectorizer.fit(dataset["request"])
label_encoder = LabelEncoder()
label_encoder.fit(dataset["tags"])

# model
model = tf.keras.models.load_model("haul.h5") 

def predict(sentence):
    prediction = model.predict(vectorizer.transform([sentence]).toarray())
    intent = label_encoder.inverse_transform([prediction.argmax()])
    return dataset[dataset["tags"] == intent[0]]["responses"].tolist()[0]

app = Flask(__name__)
app.config["SECRET_KEY"] = "7h!$i$^34y$3C43T73Y"
socket = SocketIO(app)
app.permanent_session_lifetime = timedelta(minutes=10)

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        if "email" in session:
            return redirect(url_for("haul"))
        return render_template("login.html")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # print(f"\n\n\n\n{email}, {password}\n\n\n\n")
        data = DB.fetchValues(email, password)
        print(f"\n\n\n{data}\n\n\n")
        if data is not None:
            session["email"] = email
            return redirect(url_for("haul"))
        else:
            flash("Invalid username or password !", "info")
            return redirect(url_for("login_page"))

@app.route("/register", methods=["GET", "POST"])
def signup_page():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        flash("Sucessfully created !", "info")
        # print(f"\n\n\n\n{username}, {email}, {password}\n\n\n\n")
        DB.insertValues(username, email, password)

        return redirect(url_for("login_page"))

@app.route("/haul", methods=["GET", "POST"])
def haul():
    if request.method == "GET":
        if "email" in session:
            flash("logged in", "info")
            return render_template("haul.html")
        return redirect(url_for("login_page"))
    return redirect(url_for("login_page"))

@socket.on("user-input")
def handle_user_input(user_input):
    print(f"\n\nuser input: {user_input["data"]}\n\n")
    if user_input["data"].lower() == "who is my best friend":
        emit("bot-response", "Harini is your best friend 🙌")
    elif user_input["data"].lower() == "say about harini":
        emit("bot-response", "Harini is cute young barbie doll 😊")
    elif user_input["data"].lower() == "what is my dream":
        emit("bot-response", "to be a good husband to your wife 🔥")
    else:
        # print(f"\n\nmodel prediction: ", predict(user_input["data"]), "\n\n")
        emit("bot-response", predict(user_input["data"]))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)

