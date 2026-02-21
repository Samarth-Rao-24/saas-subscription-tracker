from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from app.extensions import db
from app.models.subscription import Subscription
from datetime import datetime
import csv
from io import StringIO

subscription = Blueprint("subscription", __name__)


# ----------------------------------
# Add Subscription
# ----------------------------------
@subscription.route("/add-subscription", methods=["GET", "POST"])
@login_required
def add_subscription():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            price = request.form.get("price")
            billing_date = request.form.get("billing_date")
            category = request.form.get("category")
            frequency = request.form.get("frequency")

            new_sub = Subscription(
                name=name,
                price=float(price),
                billing_date=datetime.strptime(billing_date, "%Y-%m-%d").date(),
                category=category,
                frequency=frequency,
                user=current_user
            )

            db.session.add(new_sub)
            db.session.commit()

            flash("Subscription added successfully.", "success")
            return redirect(url_for("dashboard"))

        except Exception as e:
            db.session.rollback()
            print("ADD SUB ERROR:", e)
            flash("Something went wrong while adding subscription.", "danger")
            return redirect(url_for("subscription.add_subscription"))

    return render_template("add_subscription.html")


# ----------------------------------
# Delete Subscription
# ----------------------------------
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


# ----------------------------------
# Edit Subscription
# ----------------------------------
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
            ).date()
            sub.category = request.form.get("category")
            sub.frequency = request.form.get("frequency")

            db.session.commit()

            flash("Subscription updated successfully.", "success")
            return redirect(url_for("dashboard"))

        except Exception as e:
            db.session.rollback()
            print("EDIT SUB ERROR:", e)
            flash("Something went wrong while updating.", "danger")
            return redirect(url_for("subscription.edit_subscription", id=id))

    return render_template("edit_subscription.html", sub=sub)


# ----------------------------------
# Export Subscriptions (CSV)
# ----------------------------------
@subscription.route("/export")
@login_required
def export_subscription():
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()

    si = StringIO()
    writer = csv.writer(si)

    # ✅ Added Frequency column
    writer.writerow(["Name", "Category", "Price", "Frequency", "Billing Date"])

    for sub in subscriptions:
        writer.writerow([
            sub.name,
            sub.category,
            sub.price,
            sub.frequency,
            sub.billing_date.strftime("%Y-%m-%d") if sub.billing_date else ""
        ])

    output = si.getvalue()

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=subscriptions.csv"}
    )