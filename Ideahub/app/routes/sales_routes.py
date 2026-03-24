from flask import Blueprint, jsonify
from datetime import datetime
from decimal import Decimal
from app.utils.auth import login_required

from app.models import Transaction


# Blueprint for sales routes
sales_bp = Blueprint("sales_routes", __name__)


# ----------------------------------
# DAILY SALES SUMMARY
# ----------------------------------
@sales_bp.route("/api/daily-sales")
@login_required
def daily_sales():

    today = datetime.utcnow().date()

    transactions = Transaction.query.all()

    total_revenue = Decimal("0.00")
    total_food = Decimal("0.00")
    total_space = Decimal("0.00")

    transaction_count = 0

    for t in transactions:

        if t.created_at.date() == today:

            total_revenue += t.total_bill
            total_food += t.food_bill
            total_space += t.time_bill
            transaction_count += 1

    return jsonify({
        "date": str(today),
        "transactions": transaction_count,
        "total_revenue": float(total_revenue),
        "space_revenue": float(total_space),
        "food_revenue": float(total_food)
    })