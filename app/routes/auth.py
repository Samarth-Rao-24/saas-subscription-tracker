from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app.extensions import db



auth=Blueprint("auth",__name__,url_prefix='/auth')

@auth.route("/signup", methods=['GET','POST'])
def signup():
    if request.method=="POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")

        existing_user=User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered")
            return redirect(url_for("auth.signup"))

        hashed_password=generate_password_hash(password)

        new_user=User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!")
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html")

@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))

        flash("Invalid credentials")

    return render_template("auth/login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))