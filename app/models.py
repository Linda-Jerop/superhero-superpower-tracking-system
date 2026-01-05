from app import db
from sqlalchemy.orm import validates

class Hero(db.Model):
    __tablename__ = 'heroes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)
    
    # Relationships
    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete-orphan') # no circular refs go crazy
    
    def to_dict(self, include_hero_powers=False):
        """Serialize Hero to dictionary, optionally including hero_powers"""
        data = {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
        }
        if include_hero_powers:
            data['hero_powers'] = [hp.to_dict(include_hero=False) for hp in self.hero_powers] # depth control moment
        return data


class Power(db.Model):
    __tablename__ = 'powers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    # Relationships
    hero_powers = db.relationship('HeroPower', backref='power', cascade='all, delete-orphan') # no infinite loops fr
    
    @validates('description')
    def validate_description(self, key, value):
        """Validate that description exists and is at least 20 chars"""
        if not value or len(value) < 20:
            raise ValueError("description must be present and at least 20 characters long")
        return value
    
    def to_dict(self):
        """Serialize Power to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    
    @validates('strength')
    def validate_strength(self, key, value):
        """Validate that strength is one of the allowed values"""
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:
            raise ValueError(f"strength must be one of {valid_strengths}")
        return value
    
    def to_dict(self, include_hero=True, include_power=True):
        """Serialize HeroPower to dictionary with relationship control"""
        data = {
            'id': self.id,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'strength': self.strength,
        }
        if include_hero:
            data['hero'] = self.hero.to_dict() # just the basics, no infinite scroll
        if include_power:
            data['power'] = self.power.to_dict()
        return data
