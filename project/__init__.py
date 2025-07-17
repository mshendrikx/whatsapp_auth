import os

from flask import Flask, request
from flask_babel import Babel, gettext as _
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine, text

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
babel = Babel()

def get_locale():

    # Get language from current user
    if current_user.is_authenticated == True:
        lang = current_user.language
    # Try to get the locale from the URL parameter 'lang'
    elif request.args.get("lang"):
        lang = request.args.get("lang")
    else:
        lang = request.accept_languages.best_match(["en", "pt"])
    # If no 'lang' parameter, use the Accept-Languages header
    return lang

def create_app():
    
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.urandom(24).hex()
    
    app.config["BABEL_DEFAULT_LOCALE"] = "en"  # Default language
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "./translations"
    
    db_user = os.environ.get("DB_USERNAME")
    db_pass = os.environ.get("DB_PASSWORD")
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    db_name = os.environ.get("DB_DATABASE")

    # Connect to MySQL server (without specifying database)
    server_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/"
    engine = create_engine(server_url)
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
    
    db_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    
    db.init_app(app)

    babel.init_app(app, locale_selector=get_locale)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    
    with app.app_context():
        # Create the database tables if they don't exist
        db.create_all()
            # add admin user to the database
        user = User.query.filter_by(id=1).first()
        if not user:
            new_user = User(
                id=1,
                mobile="+5599999999999",
                name="Admin",
                email="admin@admin.com",
                password=generate_password_hash("admin", method="pbkdf2:sha256"),
                language="en",
                theme ="dark",
                admin=1
            )
            db.session.add(new_user)
            db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
