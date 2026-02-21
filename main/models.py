from main.extensions import db
from datetime import datetime


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    max_load = db.Column(db.Integer, nullable=False)
    odometer = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Available")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    maintenances = db.relationship("Maintenance", backref="vehicle", lazy=True)
    expenses = db.relationship('Expense', backref='vehicle', lazy=True)
    trips = db.relationship("Trip", backref="vehicle", lazy=True)

    def __repr__(self):
        return f"<Vehicle {self.name} ({self.license_plate})>"
    
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable=False)
    driver = db.Column(db.String(50), nullable=False)
    cargo_weight = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="Draft")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    license_expiry = db.Column(db.Date, nullable=False)
    completion_rate = db.Column(db.Integer, default=0)  # 0-100 %
    safety_score = db.Column(db.Integer, default=0)      # 0-100 %
    status = db.Column(db.String(20), default="On Duty") 
    
    
class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    details = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    expense_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)