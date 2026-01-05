from flask import Blueprint, request, jsonify
from app import db
from app.models import Hero, Power, HeroPower
from app.email import send_hero_power_email
from sqlalchemy.exc import IntegrityError

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
        return jsonify(hero_power.to_dict()), 201 # lowkey a vibe
    except ValueError as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400


# ============= EMAIL ROUTE =============

@api_bp.route('/send_power_email', methods=['POST'])
def send_power_email():
    """Send email notification about a new power acquisition"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not all(k in data for k in ['hero_name', 'power_name', 'recipient_email']):
        return jsonify({'errors': ['hero_name, power_name, and recipient_email are required']}), 400
    
    try:
        success = send_hero_power_email(
            data['hero_name'],
            data['power_name'],
            data['recipient_email']
        )
        
        if success:
            return jsonify({'message': 'Email sent successfully'}), 200
        else:
            return jsonify({'errors': ['Failed to send email']}), 500
    except Exception as e:
        return jsonify({'errors': [str(e)]}), 400

