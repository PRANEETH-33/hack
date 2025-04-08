from flask import Flask, render_template, request, redirect, url_for, flash
import random
import os

from utils.db import db
from models.models import Contact

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flashing messages

# DB Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthwellness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Global state
mood = ""
habits = []
wellness_tips = [
    "Drink a glass of water.",
    "Take a short walk.",
    "Practice deep breathing.",
    "Stretch for 5 minutes.",
    "Write down something you're grateful for."
]

# Create tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

# Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    global mood, habits

    if request.method == "POST":
        if "mood" in request.form:
            mood = request.form["mood"]
        elif "habit" in request.form:
            habits.append(request.form["habit"])
        elif "delete" in request.form:
            try:
                habits.pop(int(request.form["delete"]))
            except (IndexError, ValueError):
                pass

    tip = random.choice(wellness_tips)
    return render_template("index.html", mood=mood, habits=habits, tip=tip)

# About Page
@app.route("/about")
def about():
    return render_template("about-us.html")

# Services Page
@app.route("/services")
def services():
    return render_template("services.html")

# Blog Page
@app.route("/blog")
def blog():
    return render_template("blog.html")

# Contact Page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if name and email and message:
            contact_data = Contact(name=name, email=email, message=message)
            db.session.add(contact_data)
            db.session.commit()
            flash("Message sent successfully!", "success")
            return redirect(url_for("contact"))
        else:
            flash("All fields are required!", "error")

    return render_template("contact.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)  # Use this to avoid the signal error
