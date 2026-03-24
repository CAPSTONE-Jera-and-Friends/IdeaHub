from datetime import datetime
from app import db

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_session_id = db.Column(db.Integer, db.ForeignKey("customer_sessions.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    session = db.relationship("CustomerSession", backref="orders")