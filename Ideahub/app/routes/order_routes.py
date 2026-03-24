from flask import Blueprint, jsonify, request, render_template
from decimal import Decimal
from app.utils.auth import login_required

from app import db
from app.models import Order, OrderItem, MenuItem, CustomerSession


# Blueprint for order related routes
order_bp = Blueprint("order_routes", __name__)


# ----------------------------------
# GET MENU ITEMS
# ----------------------------------
@order_bp.route("/api/menu")
@login_required
def get_menu():

    items = MenuItem.query.all()

    result = []

    for item in items:
        result.append({
            "id": item.id,
            "name": item.name,
            "price": float(item.price),
            "category": item.category
        })

    return jsonify(result)


# ----------------------------------
# ADD ORDER
# ----------------------------------
@order_bp.route("/api/add-order", methods=["POST"])
@login_required
def add_order():

    data = request.get_json()

    session_id = data.get("session_id")
    items = data.get("items")

    if not session_id or not items:
        return jsonify({"error": "session_id and items are required"}), 400

    session = CustomerSession.query.get(session_id)

    if not session:
        return jsonify({"error": "Session not found"}), 404

    # create order
    new_order = Order(customer_session_id=session_id)

    db.session.add(new_order)
    db.session.commit()

    # add items
    for item in items:

        menu_item = MenuItem.query.get(item["menu_item_id"])

        if not menu_item:
            continue

        order_item = OrderItem(
            order_id=new_order.id,
            menu_item_id=menu_item.id,
            quantity=item.get("quantity", 1),
            price=menu_item.price
        )

        db.session.add(order_item)

    db.session.commit()

    return jsonify({
        "message": "Order added successfully",
        "order_id": new_order.id
    })


# ----------------------------------
# GET SESSION ORDERS
# ----------------------------------
@order_bp.route("/api/session-orders/<int:session_id>")
@login_required
def get_session_orders(session_id):

    orders = Order.query.filter_by(customer_session_id=session_id).all()

    order_list = []
    food_total = Decimal("0.00")

    for order in orders:

        for item in order.items:

            total_price = item.quantity * item.price
            food_total += total_price

            order_list.append({
            "id": item.id,
            "item_name": item.menu_item.name,
            "quantity": item.quantity,
            "price": float(item.price),
            "total": float(total_price)
        })

    return jsonify({
        "session_id": session_id,
        "orders": order_list,
        "food_total": float(food_total)
    })


@order_bp.route("/order/<int:session_id>")
@login_required
def order_page(session_id):
    return render_template("order.html", session_id=session_id)


@order_bp.route("/api/void-item/<int:item_id>", methods=["DELETE"])
@login_required
def void_item(item_id):

    item = OrderItem.query.get(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Item voided successfully"})

