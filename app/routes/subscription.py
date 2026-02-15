from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Subscription
from datetime import datetime

subscription = Blueprint('subscription', __name__)

@subscription.route('/add-subscription', methods=["GET", "POST"])
@login_required
def add_subscription():
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        billing_date = request.form.get("billing_date")

        try:    
            new_sub = Subscription(
                name=name,
                price=float(price),
                billing_date=datetime.strptime(billing_date, "%Y-%m-%d"),
                owner=current_user
            )

            db.session.add(new_sub)
            db.session.commit()

            flash("Subscription added successfully")
            return redirect(url_for("dashboard"))
        
        except Exception as e:
            db.session.rollback()
            print("🔥 ERROR:", e)
            raise e

    return render_template("add_subscription.html")
