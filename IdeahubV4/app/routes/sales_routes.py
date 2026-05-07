from flask import Blueprint, jsonify, request, session
from app.utils.auth import login_required

from app.core.clock import SystemClock
from app.repositories.sales_repository import SalesRepository
from app.services.sales_service import SalesService


# Blueprint for sales routes
sales_bp = Blueprint("sales_routes", __name__)
_service = SalesService(repo=SalesRepository(), clock=SystemClock())


def admin_only_json():
    if session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    return None


# ----------------------------------
# DAILY SALES SUMMARY
# ----------------------------------
@sales_bp.route("/api/daily-sales")
@login_required
def daily_sales():
    guard = admin_only_json()
    if guard:
        return guard

    return jsonify(_service.daily_sales())


@sales_bp.route("/api/sales-summary")
@login_required
def sales_summary():
    guard = admin_only_json()
    if guard:
        return guard

    period = request.args.get("period", "today")
    return jsonify(_service.sales_summary(period))


@sales_bp.route("/api/sales-compare")
@login_required
def sales_compare():
    guard = admin_only_json()
    if guard:
        return guard

    return jsonify(_service.sales_compare())