from datetime import datetime
from app import db

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_session_id = db.Column(db.Integer, db.ForeignKey("customer_sessions.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Backward compatible: existing DB rows may still store "preparin".
    status = db.Column(db.String(20), nullable=False, default="preparing")

    session = db.relationship("CustomerSession", backref="orders")