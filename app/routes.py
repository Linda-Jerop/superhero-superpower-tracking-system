from flask import Blueprint, request, jsonify
from app import db
from app.models import Hero, Power, HeroPower

api_bp = Blueprint('api', __name__)

# Routes here (placeholder for now)
