from sqlalchemy import text
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

    insert_query = text("""
        INSERT INTO expense (date, category, amount, description)
        VALUES 
('2025/01/03', 'food', 12.45, 'Weekly grocery vegetables purchase.'),
('2025/01/05', 'toys', 18.99, 'Remote control racing car.'),
('2025/01/07', 'pets', 25.30, 'Premium dog food pack.'),
('2025/01/09', 'electronics', 199.99, 'Wireless keyboard purchase.'),
('2025/01/12', 'banking', 5.00, 'Monthly account maintenance fee.'),

('2025/01/15', 'food', 7.80, 'Bakery bread and buns.'),
('2025/01/18', 'toys', 9.50, 'Puzzle game for kids.'),
('2025/01/20', 'pets', 14.60, 'Cat litter refill pack.'),
('2025/01/22', 'electronics', 59.99, 'Bluetooth headphones.'),
('2025/01/25', 'banking', 2.50, 'ATM withdrawal charge.'),

('2025/02/01', 'food', 22.10, 'Monthly rice bag purchase.'),
('2025/02/03', 'toys', 15.75, 'Board game for family night.'),
('2025/02/05', 'pets', 32.40, 'Pet grooming kit.'),
('2025/02/08', 'electronics', 349.00, 'Smartwatch purchase.'),
('2025/02/10', 'banking', 3.25, 'Online transfer fee.'),

('2025/02/14', 'food', 11.20, 'Restaurant dinner bill.'),
('2025/02/16', 'toys', 6.99, 'Action figure toy.'),
('2025/02/18', 'pets', 18.30, 'Dog chew toys.'),
('2025/02/20', 'electronics', 89.99, 'Portable power bank.'),
('2025/02/23', 'banking', 4.75, 'Cheque processing fee.'),

('2025/03/01', 'food', 30.50, 'Supermarket monthly shopping.'),
('2025/03/03', 'toys', 12.00, 'Educational toy blocks.'),
('2025/03/05', 'pets', 45.00, 'Pet vaccination charge.'),
('2025/03/08', 'electronics', 129.99, 'Wireless mouse.'),
('2025/03/10', 'banking', 6.00, 'Credit card annual fee installment.'),

('2025/03/14', 'food', 9.90, 'Fast food takeaway.'),
('2025/03/16', 'toys', 20.00, 'Toy train set.'),
('2025/03/18', 'pets', 27.50, 'Pet bed purchase.'),
('2025/03/20', 'electronics', 499.00, 'Tablet device purchase.'),
('2025/03/22', 'banking', 1.75, 'SMS alert charges.');



    """)

    db.session.execute(insert_query)
    db.session.commit()

    print("Dummy data inserted successfully!")
