from flask import Blueprint, render_template
from flask_login import login_required
from extensions import get_db

# IMPORTANT: blueprint name MUST be history_bp
history_bp = Blueprint("history", __name__)

@history_bp.route("/history")
@login_required
def history():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT message, sender, created_at
        FROM chats
        ORDER BY created_at DESC
    """)
    chats = cur.fetchall()
    cur.close()
    db.close()

    return render_template("history.html", chats=chats)
