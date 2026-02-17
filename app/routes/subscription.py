from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Subscription
from datetime import datetime
import csv
from io import StringIO
from flask import Response

subscription = Blueprint('subscription', __name__)


@subscription.route('/add-subscription', methods=["GET", "POST"])
@login_required
def add_subscription():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            price = request.form.get("price")
            billing_date = request.form.get("billing_date")
            category = request.form.get("category")
            frequency=request.form.get("frequency")
            new_sub = Subscription(
                name=name,
                price=float(price),
                billing_date=datetime.strptime(billing_date, "%Y-%m-%d"),
                category=category,
                frequency=frequency,
                owner=current_user
            )

            db.session.add(new_sub)
            db.session.commit()

            flash("Subscription added successfully.", "success")
            return redirect(url_for("dashboard"))

        except Exception:
            db.session.rollback()
            flash("Something went wrong while adding subscription.", "danger")
            return redirect(url_for("subscription.add_subscription"))

    return render_template("add_subscription.html")


@subscription.route("/delete-subscription/<int:id>")
@login_required
def delete_subscription(id):
    sub = Subscription.query.get_or_404(id)

    if sub.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("dashboard"))

    db.session.delete(sub)
    db.session.commit()

    flash("Subscription deleted successfully.", "success")
    return redirect(url_for("dashboard"))


@subscription.route("/edit-subscription/<int:id>", methods=["GET", "POST"])
@login_required
def edit_subscription(id):
    sub = Subscription.query.get_or_404(id)

    if sub.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        try:
            sub.name = request.form.get("name")
            sub.price = float(request.form.get("price"))
            sub.billing_date = datetime.strptime(
                request.form.get("billing_date"),
                "%Y-%m-%d"
            )
            sub.category = request.form.get("category")

            db.session.commit()

            flash("Subscription updated successfully.", "success")
            return redirect(url_for("dashboard"))

        except Exception:
            db.session.rollback()
            flash("Something went wrong while updating.", "danger")
            return redirect(url_for("subscription.edit_subscription", id=id))

    return render_template("edit_subscription.html", sub=sub)


@subscription.route("/export")
@login_required
def export_subscription():
    subscriptions =Subscription.query.filter_by(user_id=current_user.id).all()

    si=StringIO()
    writer=csv.writer(si)

    writer.writerow(["Name","Category","Price","Billing Date"])

    for sub in subscriptions:
        writer.writerow([
            sub.name,
            sub.category,
            sub.price,
            sub.billing_date.strftime("%Y-%m-%d")
        ])

    output=si.getvalue()

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition":"attachment;filename=subscriptions.csv"}
    )