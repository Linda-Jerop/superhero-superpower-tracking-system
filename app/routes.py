from flask import Blueprint, request, jsonify, send_file
from app import db
from app.models import Hero, Power, HeroPower
from app.email import send_hero_assignment_email, send_power_update_email
from sqlalchemy.exc import IntegrityError
import os

api_bp = Blueprint('api', __name__)

# ============= HERO ROUTES =============

@api_bp.route('/heroes', methods=['GET'])
def get_heroes():
    """Get all heroes with basic info"""
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes]), 200


@api_bp.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    """Get specific hero with their powers"""
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    return jsonify(hero.to_dict(include_hero_powers=True)), 200 # flex with the detail


# ============= POWER ROUTES =============

@api_bp.route('/powers', methods=['GET'])
def get_powers():
    """Get all powers"""
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers]), 200


@api_bp.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    """Get specific power"""
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    return jsonify(power.to_dict()), 200


@api_bp.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    """Update power description"""
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    
    data = request.get_json()
    if not data or 'description' not in data:
        return jsonify({'errors': ['description is required']}), 400
    
    try:
        power.description = data['description'] # validation happens automatically
        db.session.commit()
        
        # Send notification email
        recipient_email = data.get('notification_email', 'admin@superheroes.com')
        send_power_update_email(power.name, recipient_email)
        
        return jsonify(power.to_dict()), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400


# ============= HERO POWER ROUTES =============

@api_bp.route('/hero_powers', methods=['POST'])
def create_hero_power():
    """Create new hero power association"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not all(k in data for k in ['strength', 'power_id', 'hero_id']):
        return jsonify({'errors': ['strength, power_id, and hero_id are required']}), 400
    
    # Check if hero and power exist
    hero = Hero.query.get(data.get('hero_id'))
    power = Power.query.get(data.get('power_id'))
    
    if not hero or not power:
        return jsonify({'errors': ['Invalid hero_id or power_id']}), 404
    
    try:
        hero_power = HeroPower(
            strength=data['strength'],
            power_id=data['power_id'],
            hero_id=data['hero_id']
        )
        db.session.add(hero_power)
        db.session.commit()
        
        # Send notification email
        recipient_email = data.get('notification_email', 'admin@superheroes.com')
        send_hero_assignment_email(hero.name, power.name, recipient_email)
        
        return jsonify(hero_power.to_dict()), 201 # lowkey a vibe
    except ValueError as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400


# ============= EMAIL DEMO ROUTE =============

@api_bp.route('/send-test-email', methods=['POST'])
def send_test_email():
    """Demo route to test email sending capability"""
    data = request.get_json()
    recipient = data.get('recipient_email', 'admin@superheroes.com')
    
    try:
        from app import mail
        from flask_mail import Message
        
        msg = Message(
            subject='Superheroes API - Test Email',
            recipients=[recipient],
            body='This is a test email from the Superheroes API. Email functionality is working!'
        )
        mail.send(msg)
        return jsonify({'message': 'Test email sent successfully', 'recipient': recipient}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to send email: {str(e)}'}), 500


# ============= TEST UI ROUTE =============

@api_bp.route('/test-ui')
def test_ui():
    """Serve the interactive test UI for all endpoints"""
    ui_path = os.path.join(os.path.dirname(__file__), '..', 'test_ui.html')
    return send_file(ui_path, mimetype='text/html')
