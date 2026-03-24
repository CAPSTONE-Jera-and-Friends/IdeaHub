from flask import Blueprint, jsonify
from app.models import User
from app.utils.auth import login_required

user_bp = Blueprint("user_routes", __name__)

@user_bp.route("/api/profile/<int:user_id>")
@login_required
def get_profile(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "name": user.full_name,
        "username": user.username,
        "role": user.role,
        "created_at": user.created_at
    })