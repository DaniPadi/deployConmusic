from flask import Flask, redirect, url_for, request
from flask_login import current_user
from extensions import db, login_manager
from auth.routes import auth_bp
from music.routes import music_bp
from models import User
from flask_wtf.csrf import CSRFProtect

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_name=None):
    app = Flask(__name__)
    csrf = CSRFProtect()
    csrf.init_app(app) 
    app.config.from_object('config.config')

    db.init_app(app)
    with app.app_context():
        db.create_all()  # Solo en desarrollo o pruebas

    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(music_bp)
    
    @app.before_request
    def redirect_to_login():
        if not current_user.is_authenticated and request.endpoint not in ['auth.login', 'auth.register']:
            return redirect(url_for('auth.login'))

    if config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
