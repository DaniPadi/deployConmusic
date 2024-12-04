from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from extensions import db

auth_bp= Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        instrument = request.form.get('instrument')

        if password != confirm_password:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"error": "Las contrasenas no coinciden."}), 400
            
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"error": "Correo ya registrado"}), 400
            return redirect(url_for('auth.register'))
        
        new_user = User(email=email, password=password, first_name=first_name, middle_name=middle_name, last_name=last_name, instrument=instrument)
        
        db.session.add(new_user)
        db.session.commit()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"message": "Usuario registrado exitosamente."}), 200
        return redirect(url_for('auth.login'))  
    return render_template('register.html')

@auth_bp.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')


        if not email or not password:
         return jsonify({"error": "Correo y contraseña son obligatorios"}), 400
        
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"message": "Usuario ingresado exitosamente."}), 200
            login_user(user)
            return redirect(url_for('music.manage_music'))
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"error": "Correo o contraseña incorrectos."}), 400
    return render_template('login.html')

@auth_bp.route('/change_password', methods= ['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        if new_password != confirm_password:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"error": "Las contraseñas no coinciden."}), 400
            return redirect(url_for('auth.change_password'))
        if current_user.password != old_password:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"error": "Contraseña actual incorrecta."}), 400
            return redirect(url_for('auth.change_password'))
        current_user.password = new_password
        db.session.commit()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"message": "Contraseña actualizada exitosamente."}), 200
        return redirect(url_for('auth.change_password'))
    return render_template('change_password.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
