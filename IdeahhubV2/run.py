from app import create_app, db, socketio
from app.models import SpaceType, MenuItem
from decimal import Decimal
from sqlalchemy import text

app = create_app()


def seed_database():
    with app.app_context():

        db.create_all() 
        # MySQL: only add column if it doesn't exist yet.
        status_cols = db.session.execute(text("""
            SELECT COLUMN_NAME
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'orders'
              AND COLUMN_NAME = 'status'
        """)).fetchall()

        if not status_cols:
            db.session.execute(text("""
                ALTER TABLE orders
                ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'preparing'
            """))
            db.session.commit()

        # Insert space types if empty
        if SpaceType.query.count() == 0:
            regular = SpaceType(name="Regular Lounge", rate_per_minute=Decimal("0.1667"))
            premium = SpaceType(name="Premium Lounge", rate_per_minute=Decimal("0.3333"))
            boardroom = SpaceType(name="Boardroom", rate_per_minute=Decimal("4.1667"))

            db.session.add_all([regular, premium, boardroom])
            db.session.commit()

        # Insert menu items if empty
        if MenuItem.query.count() == 0:
            items = [
                MenuItem(name="Juice", price=Decimal("30.00"), category="Drink"),
                MenuItem(name="Coffee", price=Decimal("40.00"), category="Drink"),
                MenuItem(name="Burger", price=Decimal("50.00"), category="Food"),
                MenuItem(name="Fries", price=Decimal("35.00"), category="Snack"),
                MenuItem(name="Adobo", price=Decimal("60.00"), category="MainDish"),
            ]

            db.session.add_all(items)
            db.session.commit()


seed_database()


if __name__ == "__main__":
    socketio.run(app, debug=True)

