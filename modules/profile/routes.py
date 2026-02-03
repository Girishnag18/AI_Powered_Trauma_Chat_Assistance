from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import get_db

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    db = get_db()
    cur = db.cursor()

    # Update name/email
    if request.method == "POST" and "name" in request.form:
        cur.execute(
            "UPDATE users SET name=%s, email=%s WHERE id=%s",
            (request.form["name"], request.form["email"], current_user.id)
        )
        db.commit()
        flash("Profile updated successfully")

    cur.execute(
        "SELECT name, email, created_at FROM users WHERE id=%s",
        (current_user.id,)
    )
    user = cur.fetchone()

    cur.close()
    db.close()

    return render_template("profile.html", user=user)


@profile_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    if new_password != confirm_password:
        flash("New passwords do not match")
        return redirect(url_for("profile.profile"))

    db = get_db()
    cur = db.cursor()

    # Get stored hashed password
    cur.execute(
        "SELECT password FROM users WHERE id=%s",
        (current_user.id,)
    )
    stored_hash = cur.fetchone()[0]

    if not check_password_hash(stored_hash, current_password):
        flash("Current password is incorrect")
        cur.close()
        db.close()
        return redirect(url_for("profile.profile"))

    # Update password
    new_hash = generate_password_hash(new_password)
    cur.execute(
        "UPDATE users SET password=%s WHERE id=%s",
        (new_hash, current_user.id)
    )

    db.commit()
    cur.close()
    db.close()

    flash("Password changed successfully")
    return redirect(url_for("profile.profile"))
