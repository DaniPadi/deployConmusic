from flask import Flask, redirect, url_for, request
from extensions import db, login_manager
from auth.routes import auth_bp
from music.routes import music_bp
from models import User



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.config')

    db.init_app(app)
    with app.app_context():
     db.create_all()

    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(music_bp)
    
    @app.before_request
    def redirect_to_login():
        if request.path == '/':
            return redirect(url_for('auth.login'))  # Redirige a la ruta de inicio de sesión
    
    return app




if __name__=='__main__':
    app = create_app()
    app.run(debug=True)
