"""
Run this script manually to apply schema changes and seed data.
Usage: python -m app.db.run_migrations
"""

from app import create_app, db
from app.db.migrator import SchemaMigrator
from app.db.seeder import DatabaseSeeder


def main() -> None:
    app = create_app()
    with app.app_context():
        SchemaMigrator(db, app).run()
        DatabaseSeeder(db, app).run()
        print("Migration and seeding complete.")


if __name__ == "__main__":
    main()
