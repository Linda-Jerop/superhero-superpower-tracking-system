from flask import Blueprint, request, jsonify
from app import db
from app.models import Hero, Power, HeroPower

api_bp = Blueprint('api', __name__)

# Routes will be added here (placeholder for now)
