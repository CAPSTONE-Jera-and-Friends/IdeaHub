from functools import wraps
from flask import session, redirect, jsonify, flash

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

          
            if "/api/" in str(view_func):
                return jsonify({"error": "Unauthorized"}), 401

           
            flash("Please log in first!", "danger")
            return redirect("/login")

        return view_func(*args, **kwargs)

    return wrapper