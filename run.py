from flask import Flask
from database.models import db
from routes.main_routes import register_main_routes
from routes.api_routes import register_api_routes
from routes.auth_routes import register_auth_routes
from routes.profile_routes import register_profile_routes
from routes.admin_routes import register_admin_routes
from flask_login import LoginManager
from flask_mail import Mail
import config

app = Flask(__name__)

# ---------- CONFIG ----------
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# ---------- INIT DB ----------
db.init_app(app)

# ---------- FLASK LOGIN ----------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

from database.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- MAIL ----------
mail = Mail(app)

# ---------- REGISTER ROUTES ----------
register_main_routes(app)
register_api_routes(app)
register_auth_routes(app, mail)
register_profile_routes(app)
register_admin_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)