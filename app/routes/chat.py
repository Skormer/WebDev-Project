from datetime import datetime

from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_, or_

from ..extensions import db
from ..forms import MessageForm
from ..models import Message, User

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/")
@login_required
def inbox():
    """Übersicht aller Konversationen (je Gesprächspartner die letzte Nachricht)."""
    messages = (
        Message.query.filter(
            or_(Message.sender_id == current_user.id, Message.receiver_id == current_user.id)
        )
        .order_by(Message.sent_at.desc(), Message.id.desc())
        .all()
    )

    conversations = {}
    for message in messages:
        partner_id = (
            message.receiver_id if message.sender_id == current_user.id else message.sender_id
        )
        convo = conversations.setdefault(
            partner_id,
            {"partner": db.session.get(User, partner_id), "last": message, "unread": 0},
        )
        if message.receiver_id == current_user.id and message.read_at is None:
            convo["unread"] += 1

    convo_list = sorted(conversations.values(), key=lambda c: c["last"].sent_at, reverse=True)
    return render_template("chat/inbox.html", conversations=convo_list)


@chat_bp.route("/<int:user_id>", methods=["GET", "POST"])
@login_required
def conversation(user_id):
    partner = User.query.get_or_404(user_id)
    if partner.id == current_user.id:
        abort(400)

    form = MessageForm()
    if form.validate_on_submit():
        db.session.add(
            Message(
                sender_id=current_user.id,
                receiver_id=partner.id,
                body=form.body.data.strip(),
            )
        )
        db.session.commit()
        return redirect(url_for("chat.conversation", user_id=partner.id))

    messages = (
        Message.query.filter(
            or_(
                and_(Message.sender_id == current_user.id, Message.receiver_id == partner.id),
                and_(Message.sender_id == partner.id, Message.receiver_id == current_user.id),
            )
        )
        .order_by(Message.sent_at.asc(), Message.id.asc())
        .all()
    )

    # eingehende, ungelesene Nachrichten als gelesen markieren
    unread = [m for m in messages if m.receiver_id == current_user.id and m.read_at is None]
    if unread:
        for message in unread:
            message.read_at = datetime.utcnow()
        db.session.commit()

    return render_template(
        "chat/conversation.html", partner=partner, messages=messages, form=form
    )


@chat_bp.route("/<int:user_id>/messages")
@login_required
def conversation_messages(user_id):
    """JSON-Endpoint fürs Polling: neue Nachrichten nach ``after``-ID (5s-Refresh im Frontend)."""
    partner = User.query.get_or_404(user_id)
    if partner.id == current_user.id:
        abort(400)

    after = request.args.get("after", default=0, type=int)
    messages = (
        Message.query.filter(
            or_(
                and_(Message.sender_id == current_user.id, Message.receiver_id == partner.id),
                and_(Message.sender_id == partner.id, Message.receiver_id == current_user.id),
            ),
            Message.id > after,
        )
        .order_by(Message.id.asc())
        .all()
    )

    # eingehende neue Nachrichten als gelesen markieren
    changed = False
    for message in messages:
        if message.receiver_id == current_user.id and message.read_at is None:
            message.read_at = datetime.utcnow()
            changed = True
    if changed:
        db.session.commit()

    return jsonify(messages=[
        {
            "id": m.id,
            "mine": m.sender_id == current_user.id,
            "body": m.body,
            "time": m.sent_at.strftime("%d.%m.%Y %H:%M"),
            "read": m.read_at is not None,
        }
        for m in messages
    ])
