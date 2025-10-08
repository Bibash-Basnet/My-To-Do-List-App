from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User  # make sure User model is imported

auth_bp = Blueprint('auth', __name__)

# ---------- Register ----------
@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Try another one.', 'danger')
            return redirect(url_for('auth.register'))

        # Save plain password (for learning purpose only)
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration Successful! You can now login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# ---------- Login ----------
@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  # simple comparison
            session['user'] = username
            flash('Login Successful!', 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('Invalid Username or Password', 'danger')

    return render_template('login.html')


# ---------- Logout ----------
@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged Out', 'info')
    return redirect(url_for('auth.login'))
