from flask import Blueprint, render_template
from flask_login import login_required
from extensions import get_db

# IMPORTANT: blueprint name MUST be admin_bp
admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
@login_required
def admin_dashboard():
    db = get_db()
    cur = db.cursor()

    # Get users count
    cur.execute("SELECT COUNT(*) FROM users")
    users_count = cur.fetchone()[0]

    # Get high / critical reports
    cur.execute("""
        SELECT users.name, trauma_reports.score, trauma_reports.severity, trauma_reports.created_at
        FROM trauma_reports
        JOIN users ON users.id = trauma_reports.user_id
        WHERE trauma_reports.severity IN ('High', 'Critical')
        ORDER BY trauma_reports.created_at DESC
    """)
    reports = cur.fetchall()

    cur.close()
    db.close()

    return render_template(
        "admin.html",
        users_count=users_count,
        reports=reports
    )
