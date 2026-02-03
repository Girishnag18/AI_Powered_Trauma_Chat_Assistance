from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from extensions import get_db
from .ai_engine import analyze, reply

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat")
@login_required
def chat():
    return render_template("chat.html")

@chat_bp.route("/chat/send", methods=["POST"])
@login_required
def send():
    text = request.json["message"]
    score, severity = analyze(text)
    ai_reply = reply(severity)

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO chats (user_id,message,sender) VALUES (%s,%s,'user')",
        (current_user.id, text)
    )
    cur.execute(
        "INSERT INTO chats (user_id,message,sender) VALUES (%s,%s,'ai')",
        (current_user.id, ai_reply)
    )
    cur.execute(
        "INSERT INTO trauma_reports (user_id,score,severity) VALUES (%s,%s,%s)",
        (current_user.id, score, severity)
    )

    db.commit()
    cur.close()
    db.close()

    return jsonify({
        "reply": ai_reply,
        "score": score,
        "severity": severity
    })
