from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
import os
import json
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"

USER_FILE = "users.xlsx"
CHAT_FILE = "chats.json"

# Initialize users.xlsx
if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["Full Name", "Username", "Password"])
    df.to_excel(USER_FILE, index=False)

# Initialize chats.json
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w") as f:
        json.dump([], f)

# Function to delete messages older than 1 minute
def delete_old_messages():
    while True:
        time.sleep(60)  # Runs every 1 minute
        with open(CHAT_FILE, "r+") as f:
            messages = json.load(f)
            one_minute_ago = datetime.now() - timedelta(minutes=1)
            messages = [msg for msg in messages if datetime.strptime(msg["Timestamp"], "%Y-%m-%d %H:%M:%S") > one_minute_ago]
            f.seek(0)
            json.dump(messages, f, indent=4)
            f.truncate()

# Start auto-delete thread
threading.Thread(target=delete_old_messages, daemon=True).start()

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        df = pd.read_excel(USER_FILE)
        if username in df["Username"].astype(str).tolist():
            return "Username already exists."
        df.loc[len(df)] = [full_name, username, password]
        df.to_excel(USER_FILE, index=False)
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        df = pd.read_excel(USER_FILE)
        df.columns = df.columns.str.strip()
        df["Username"] = df["Username"].astype(str).str.strip()
        df["Password"] = df["Password"].astype(str).str.strip()

        user_row = df[df["Username"] == username]
        if not user_row.empty and user_row.iloc[0]["Password"] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        return "Invalid username or password."
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    df = pd.read_excel(USER_FILE)
    users = df["Username"].tolist()
    users.remove(session["user"])
    return render_template("dashboard.html", username=session["user"], users=users)
@app.route('/terms')
def terms():
    return render_template('terms.html')
@app.route("/send_message", methods=["POST"])
def send_message():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 403
    data = request.json
    sender = session["user"]
    recipient = data.get("recipient")
    message = data.get("message")
    if not recipient or not message:
        return jsonify({"error": "Invalid data"}), 400
    with open(CHAT_FILE, "r+") as f:
        messages = json.load(f)
        messages.append({"Sender": sender, "Recipient": recipient, "Message": message, "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        f.seek(0)
        json.dump(messages, f, indent=4)
        f.truncate()
    return jsonify({"status": "Message sent"})

@app.route("/get_messages/<recipient>")
def get_messages(recipient):
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 403
    sender = session["user"]
    with open(CHAT_FILE, "r") as f:
        messages = json.load(f)
    chat_history = [msg for msg in messages if (msg["Sender"] == sender and msg["Recipient"] == recipient) or (msg["Sender"] == recipient and msg["Recipient"] == sender)]
    return jsonify(chat_history)
@app.route('/search_users', methods=['GET'])
def search_users():
    if "user" not in session:
        return jsonify([]) 
    query = request.args.get('q', '').strip().lower()
    logged_in_user = session["user"]

    df = pd.read_excel(USER_FILE)
    df.columns = df.columns.str.strip()
    df["Username"] = df["Username"].astype(str).str.strip()

    # Filter usernames that match the query and exclude the logged-in user
    matched_users = df[(df["Username"].str.lower().str.contains(query, na=False)) & (df["Username"] != logged_in_user)]["Username"].tolist()

    return jsonify(matched_users)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

