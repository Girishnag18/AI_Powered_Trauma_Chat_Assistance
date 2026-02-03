from flask import Blueprint, render_template
from flask_login import login_required, current_user
from extensions import get_db

trauma_bp = Blueprint("trauma", __name__)

@trauma_bp.route("/trauma-report")
@login_required
def trauma_report():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT score, severity, created_at
        FROM trauma_reports
        WHERE user_id=%s
        ORDER BY created_at DESC
        LIMIT 1
    """, (current_user.id,))
    report = cur.fetchone()
    cur.close()
    db.close()

    return render_template("trauma_report.html", report=report)
