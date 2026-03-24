from flask import Blueprint, render_template, request, jsonify, session, redirect
from app.models import User

bp = Blueprint("auth", __name__)

@bp.route("/login")
def login_page():

    if "user_id" in session:
        return redirect("/dashboard")

    return render_template("login.html")


@bp.route("/api/login", methods=["POST"])
def login_api():

    data = request.get_json()

    user = User.query.filter_by(username=data["username"]).first()

    if user and user.check_password(data["password"]):

        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role

        return jsonify({"message": "Login successful"})

    return jsonify({"error": "Invalid credentials"}), 401


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")