# main/routes.py

from flask import Flask, render_template, request, redirect, url_for, session, flash
from main.extensions import db
from main.models import Vehicle, Trip, Maintenance, Expense, Driver
from datetime import datetime

# Sample users (for prototype)
users = {
    "manager@example.com": {"password": "manager123", "role": "Manager"},
    "dispatcher@example.com": {"password": "dispatcher123", "role": "Dispatcher"}
}

# -----------------------
# Home Route
# -----------------------
def home():
    return redirect(url_for("login"))

# -----------------------
# Dashboard Route
# -----------------------
def dashboard():
    if "user" not in session:
        flash("Please login first!")
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# -----------------------
# Login & Logout Routes
# -----------------------
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        selected_role = request.form.get("role")  # Role from form

        if email in users and users[email]["password"] == password:
            user_role = users[email]["role"]
            if selected_role and selected_role.lower() != user_role.lower():
                flash(f"You selected the wrong role! Your role is {user_role}.")
                return redirect(url_for("login"))

            session["user"] = email
            session["role"] = user_role
            return redirect(url_for("dashboard"))

        else:
            flash("Invalid email or password")
            return redirect(url_for("login"))

    return render_template("login.html")


def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect(url_for("login"))


# -----------------------
# Vehicles Routes
# -----------------------
def vehicles_page():
    if "user" not in session:
        flash("Please login first!")
        return redirect(url_for("login"))

    if request.method == "POST":
        # Get data from form
        name = request.form.get("vehicleName")
        license_plate = request.form.get("licensePlate")
        max_load = request.form.get("maxLoad")
        odometer = request.form.get("odometer")
        status = request.form.get("vehicleStatus")

        # Create a new Vehicle instance
        new_vehicle = Vehicle(
            name=name,
            license_plate=license_plate,
            max_load=int(max_load),
            odometer=int(odometer),
            status=status
        )

        db.session.add(new_vehicle)
        db.session.commit()
        flash(f"Vehicle '{name}' added successfully!")
        return redirect(url_for("vehicles_page"))

    # GET: fetch all vehicles
    vehicles = Vehicle.query.all()
    return render_template("vehicles.html", vehicles=vehicles)


# -----------------------
# Trips Routes
# -----------------------
def trips_page():
    vehicles = Vehicle.query.all()
    drivers = ["Alex", "Maria", "John", "Sara"]  # static list for now
    trips = Trip.query.order_by(Trip.created_at.desc()).all()
    return render_template("trips.html", vehicles=vehicles, drivers=drivers, trips=trips)


def add_trip():
    vehicle_id = request.form.get("vehicle")
    driver = request.form.get("driver")
    cargo_weight = request.form.get("cargo_weight")

    if not vehicle_id or not driver or not cargo_weight:
        flash("All fields are required!", "danger")
        return redirect(url_for("trips_page"))

    try:
        cargo_weight = int(cargo_weight)
    except ValueError:
        flash("Cargo weight must be a number!", "danger")
        return redirect(url_for("trips_page"))

    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        flash("Vehicle not found!", "danger")
        return redirect(url_for("trips_page"))

    if cargo_weight > vehicle.max_load:
        flash(f"Cargo exceeds max load ({vehicle.max_load} kg)!", "danger")
        return redirect(url_for("trips_page"))

    new_trip = Trip(
        vehicle_id=vehicle.id,
        driver=driver,
        cargo_weight=cargo_weight,
        status="Draft",
        created_at=datetime.now()
    )

    db.session.add(new_trip)
    db.session.commit()
    flash("Trip assigned successfully!", "success")
    return redirect(url_for("trips_page"))


# -----------------------
# Maintenance Routes
# -----------------------
def maintenance_page():
    # Fetch vehicles that are available (not in maintenance)
    vehicles = Vehicle.query.filter(Vehicle.status != "In Shop").all()
    
    # Fetch all maintenance logs
    maintenances = Maintenance.query.order_by(Maintenance.created_at.desc()).all()
    
    return render_template(
        "maintainence.html", 
        vehicles=vehicles, 
        maintenances=maintenances
    )

def add_maintenance():
    vehicle_id = request.form.get("vehicle")
    details = request.form.get("details")

    # Check if vehicle exists
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        flash("Vehicle not found!", "danger")
        return redirect(url_for("maintenance_page"))

    # Prevent adding maintenance for a vehicle already in shop
    if vehicle.status == "In Shop":
        flash(f"{vehicle.name} is already in maintenance!", "warning")
        return redirect(url_for("maintenance_page"))

    # Add maintenance log
    maintenance = Maintenance(
        vehicle_id=vehicle.id,
        details=details,
        created_at=datetime.now()
    )
    db.session.add(maintenance)

    # Update vehicle status
    vehicle.status = "In Shop"
    db.session.commit()

    flash(f"Maintenance log added for {vehicle.name}", "success")
    return redirect(url_for("maintenance_page"))

# -----------------------
# Expenses Routes
# -----------------------
def expenses_page():
    vehicles = Vehicle.query.all()
    expenses = Expense.query.order_by(Expense.created_at.desc()).all()

    total_costs = {v.id: sum(e.amount for e in Expense.query.filter_by(vehicle_id=v.id).all()) for v in vehicles}

    return render_template('expenses.html', vehicles=vehicles, expenses=expenses, total_costs=total_costs)


def add_expense():
    vehicle_id = request.form['vehicle']
    expense_type = request.form['expense_type']
    amount = float(request.form['amount'])

    expense = Expense(vehicle_id=vehicle_id, expense_type=expense_type, amount=amount)
    db.session.add(expense)
    db.session.commit()
    flash("Expense added successfully!", "success")
    return redirect(url_for('expenses_page'))


# -----------------------
# Drivers Routes
# -----------------------
def drivers_page():
    if request.method == "POST":
        driver_id = request.form.get("driver_id")
        new_status = request.form.get(f"status_{driver_id}")
        driver = Driver.query.get(driver_id)
        if driver:
            driver.status = new_status
            db.session.commit()
            flash(f"{driver.name}'s status updated to {new_status}", "success")
        return redirect(url_for("drivers_page"))

    drivers = Driver.query.order_by(Driver.name).all()
    return render_template("drivers.html", drivers=drivers, now=datetime.now())


# -----------------------
# Operational Analytics Route
# -----------------------
def operational_analytics():
    return render_template("operational_analytics.html")


# -----------------------
# Forgot Password Route
# -----------------------
def forgot_password():
    email = request.form.get("email")
    if email in users:
        flash(f"Reset link sent to {email} (placeholder)")
    else:
        flash("Email not found!")
    return redirect(url_for("login"))


# -----------------------
# Function to register routes with app
# -----------------------
def register_routes(app: Flask):
    app.add_url_rule("/", "home", home)
    app.add_url_rule("/dashboard", "dashboard", dashboard)
    app.add_url_rule("/login", "login", login, methods=["GET", "POST"])
    app.add_url_rule("/logout", "logout", logout)
    
    app.add_url_rule("/vehicles", "vehicles_page", vehicles_page, methods=["GET", "POST"])
    app.add_url_rule("/trips", "trips_page", trips_page)
    app.add_url_rule("/trips/add", "add_trip", add_trip, methods=["POST"])
    
    app.add_url_rule("/maintenance", "maintenance_page", maintenance_page)
    app.add_url_rule("/maintenance/add", "add_maintenance", add_maintenance, methods=["POST"])
    
    app.add_url_rule("/expenses", "expenses_page", expenses_page)
    app.add_url_rule("/expenses/add", "add_expense", add_expense, methods=["POST"])
    
    app.add_url_rule("/drivers", "drivers_page", drivers_page, methods=["GET", "POST"])
    
    app.add_url_rule("/analytics", "operational_analytics", operational_analytics)
    app.add_url_rule("/forgot_password", "forgot_password", forgot_password, methods=["POST"])