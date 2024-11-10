#app.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import json

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session

from werkzeug.security import generate_password_hash, check_password_hash

from config import db  # Import db from config.py
from models import User  # Ensure this doesn't cause a circular import

from werkzeug.security import generate_password_hash, check_password_hash
from game import GameState, Hex, HexGrid  # Ensure these imports are from the right file


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


game_state = GameState()
hex_grid = HexGrid()

@app.route('/')
def index():
    return render_template('index.html')




# Example for user registration with password hashing
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken, please choose a different one.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/api/move', methods=['POST'])
def move():
    data = request.json
    q, r = data['q'], data['r']
    player_id = "player1"  # Ensure this ties to actual player logic

    # Attempt to move the player
    new_position = Hex(q, r)
    if game_state.move_entity(player_id, new_position):
        return jsonify({"success": True, "position": {"q": q, "r": r}})
    return jsonify({"success": False, "message": "Invalid move"})


@app.route('/api/combat', methods=['POST'])
def combat():
    data = request.json
    attacker_id = data.get('attacker')
    defender_id = data.get('defender')

    attacker = game_state.get_entity(attacker_id)
    defender = game_state.get_entity(defender_id)

    if not attacker or not defender:
        return jsonify({"error": "Invalid entities"}), 400

    attack_roll = attacker.roll_attack()
    if attack_roll >= defender.armor_class:
        damage = attacker.calculate_damage()
        defender.take_damage(damage)
        return jsonify({
            "hit": True,
            "damage": damage,
            "roll": attack_roll,
            "defender_health": defender.health
        })

    return jsonify({
        "hit": False,
        "damage": 0,
        "roll": attack_roll,
        "defender_health": defender.health
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)