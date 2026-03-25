from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from decimal import Decimal
from app.utils.auth import login_required

from app import db, socketio
from app.models import CustomerSession, SpaceType, Order, Transaction


# Blueprint groups related routes together
session_bp = Blueprint("session_routes", __name__)


# -----------------------------
# CHECK-IN CUSTOMER
# -----------------------------
@session_bp.route("/api/checkin", methods=["POST"])
#@login_required
def checkin():

    data = request.get_json()

    customer_name = data.get("customer_name")
    school = data.get("school")
    course = data.get("course")
    space_type_id = data.get("space_type_id")

    new_session = CustomerSession(
    customer_name=customer_name,
    school=school,
    course=course,
    space_type_id=space_type_id,
    time_in=datetime.utcnow(),  
    status="active"
)

    db.session.add(new_session)
    db.session.commit()

    return jsonify({
        "message": "Customer checked in successfully",
        "session_id": new_session.id
    })


# -----------------------------
# GET ACTIVE SESSIONS
# (LIVE RUNNING BILL)
# -----------------------------
@session_bp.route("/api/active-sessions")
@login_required
def get_active_sessions():

    sessions = CustomerSession.query.filter_by(status="active").all()

    result = []

    for session in sessions:

        now = datetime.utcnow()

        time_difference = now - session.time_in
        minutes_used = time_difference.total_seconds() / 60

        rate = session.space_type.rate_per_minute

        current_bill = (Decimal(str(minutes_used)) * rate).quantize(Decimal("0.01"))

        result.append({
        "session_id": session.id,
        "customer_name": session.customer_name,
        "school": session.school,
        "course": session.course,
        "space_type": session.space_type.name,
        "time_in": (session.time_in + timedelta(hours=8)).strftime("%B %d, %Y %I:%M %p"),
        "seconds_used": int(time_difference.total_seconds()),
        "current_bill": float(current_bill)
    })

    return jsonify(result)


# -----------------------------
# CHECKOUT CUSTOMER
# -----------------------------
@session_bp.route("/api/checkout/<int:session_id>", methods=["POST"])
@login_required
def checkout(session_id):

    session = CustomerSession.query.get(session_id)

    if not session:
        return jsonify({"error": "Session not found"}), 404

    if session.status == "completed":
        return jsonify({"error": "Session already checked out"}), 400

    # record time out
    # Store timestamps in UTC; UI adds +8 hours only when formatting.
    session.time_out = datetime.utcnow()

    # calculate total minutes
    time_difference = session.time_out - session.time_in
    total_minutes = time_difference.total_seconds() / 60

    rate_per_minute = session.space_type.rate_per_minute

    # calculate time bill
    time_bill = (Decimal(str(total_minutes)) * rate_per_minute).quantize(Decimal("0.01"))

    # calculate food bill
    food_total = Decimal("0.00")

    orders = Order.query.filter_by(customer_session_id=session_id).all()

    for order in orders:
        for item in order.items:
            food_total += item.quantity * item.price

    # calculate total bill
    total_bill = (time_bill + food_total).quantize(Decimal("0.01"))

    # create transaction record
    new_transaction = Transaction(
        session_id=session.id,
        time_bill=time_bill,
        food_bill=food_total,
        total_bill=total_bill
    )

    db.session.add(new_transaction)

    # mark session completed
    session.status = "completed"

    db.session.commit()

    socketio.emit("session_checked_out", {
        "session_id": session.id,
        "customer_name": session.customer_name,
        "space_type": session.space_type.name,
        "total_bill": float(total_bill)
    })

    return jsonify({
        "customer_name": session.customer_name,
        "minutes_used": round(total_minutes, 2),
        "rate_per_minute": float(rate_per_minute),
        "time_bill": float(time_bill),
        "food_bill": float(food_total),
        "total_bill": float(total_bill),
        "status": session.status
    })

@session_bp.route("/api/preview-checkout/<int:session_id>")
def preview_checkout(session_id):

    session = CustomerSession.query.get(session_id)

    if not session:
        return jsonify({"error": "Session not found"}), 404

    # calculate current time
    now = datetime.utcnow()
    time_difference = now - session.time_in
    total_minutes = time_difference.total_seconds() / 60

    rate_per_minute = session.space_type.rate_per_minute

    # calculate time bill
    time_bill = (Decimal(str(total_minutes)) * rate_per_minute).quantize(Decimal("0.01"))

    # calculate food bill
    food_total = Decimal("0.00")

    orders = Order.query.filter_by(customer_session_id=session_id).all()

    for order in orders:
        for item in order.items:
            food_total += item.quantity * item.price

    total_bill = (time_bill + food_total).quantize(Decimal("0.01"))

    return jsonify({
        "customer_name": session.customer_name,
        "minutes_used": total_minutes,
        "time_bill": float(time_bill),
        "food_bill": float(food_total),
        "total_bill": float(total_bill)
    })


@session_bp.route("/api/checkout-records")
@login_required
def checkout_records():

    transactions = Transaction.query.order_by(Transaction.created_at.desc()).all()
    result = []

    for tx in transactions:
        sess = tx.session
        time_in_text = (sess.time_in + timedelta(hours=8)).strftime("%B %d, %Y %I:%M %p") if sess and sess.time_in else "N/A"
        time_out_text = (sess.time_out + timedelta(hours=8)).strftime("%B %d, %Y %I:%M %p") if sess and sess.time_out else "N/A"

        seconds_spent = int((sess.time_out - sess.time_in).total_seconds()) if sess and sess.time_in and sess.time_out else None
        minutes_spent = round(seconds_spent / 60, 2) if seconds_spent is not None else None

        result.append({
            "transaction_id": tx.id,
            "customer_name": sess.customer_name if sess else "N/A",
            "space_type": sess.space_type.name if sess and sess.space_type else "N/A",
            "time_in": time_in_text,
            "time_out": time_out_text,
            "time_bill": float(tx.time_bill),
            "food_bill": float(tx.food_bill),
            "total_bill": float(tx.total_bill),
            "seconds_spent": seconds_spent,
            "minutes_spent": minutes_spent
        })

    return jsonify(result)