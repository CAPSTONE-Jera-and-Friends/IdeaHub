from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Create database object
db = SQLAlchemy()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # connect database to app
    db.init_app(app)

    # import routes
    from app.routes.session_routes import session_bp
    from app.routes.order_routes import order_bp
    from app.routes.sales_routes import sales_bp
    from app.routes.user_routes import user_bp
    from app.routes.auth_routes import bp as auth_bp
    from app.routes.dashboard_routes import bp as dashboard_bp
    from app.routes.boardroom_routes import boardroom_bp
    

    # register routes
    app.register_blueprint(session_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(boardroom_bp)
   

    @app.route("/")
    def home():
        return ("WORKING")
    return app