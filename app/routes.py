# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import app, db
from app.models import User, Bet

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return "Welcome to the Betting App"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process the form data
        # e.g., add user to the database
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form data
        return redirect(url_for('home'))  # Redirect to the home page after login
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Placeholder: Replace with actual data fetching logic
    user_bets = []  # List of bets from database
    return render_template('dashboard.html', user_bets=user_bets)


@app.route('/place_bet', methods=['GET', 'POST'])
@login_required
def place_bet():
    if request.method == 'POST':
        # Process the bet data
        amount = request.form.get('amount')
        odds = request.form.get('odds')

        # Save the bet in the database
        new_bet = Bet(user_id=current_user.id, amount=amount, odds=odds, status='Active')
        db.session.add(new_bet)
        db.session.commit()

        flash("Bet placed successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('place_bet.html')

@app.route('/admin')
@login_required
def admin():
    # Ensure the user is an admin (you can implement a role check here)
    if not current_user.is_admin:
        return redirect(url_for('dashboard'))

    # Fetch all users and bets
    users = User.query.all()
    bets = Bet.query.all()

    return render_template('admin.html', users=users, bets=bets)

@app.route('/place_bet', methods=['GET', 'POST'])
@login_required
def place_bet():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        odds = float(request.form.get('odds'))

        # Check if user has enough balance
        if amount > current_user.balance:
            flash("Insufficient balance!", "danger")
            return redirect(url_for('place_bet'))

        # Deduct the bet amount from the user's balance
        current_user.balance -= amount
        new_bet = Bet(user_id=current_user.id, amount=amount, odds=odds, status='Active')
        db.session.add(new_bet)
        db.session.commit()

        flash("Bet placed successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('place_bet.html')

# routes.py
@app.route('/resolve_bet/<int:bet_id>')
@login_required
def resolve_bet(bet_id):
    bet = Bet.query.get_or_404(bet_id)

    # Make sure the current user is the one who placed the bet
    if bet.user_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for('dashboard'))

    # Assume the result is 'win' or 'lose' for demonstration
    bet.result = 'win'  # This should be determined by your app logic
    bet.status = 'Completed'

    # Update the user's balance if they won
    if bet.result == 'win':
        current_user.balance += bet.calculate_winnings()

    db.session.commit()
    flash("Bet resolved!", "success")
    return redirect(url_for('dashboard'))


# routes.py
@app.route('/admin/resolve_bet/<int:bet_id>', methods=['POST'])
@login_required
def admin_resolve_bet(bet_id):
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('dashboard'))

    bet = Bet.query.get_or_404(bet_id)
    bet.result = request.form.get('result')  # 'win' or 'lose'
    bet.status = 'Completed'

    if bet.result == 'win':
        bet.user.balance += bet.calculate_winnings()

    db.session.commit()
    flash("Bet resolved by admin!", "success")
    return redirect(url_for('admin'))
