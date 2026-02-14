from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "description": self.description or ""
        }


def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def error(message: str, status_code: int = 400):
    return jsonify({"error": message}), status_code


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json(silent=True)
    if not data:
        return error("Request body must be valid JSON.", 400)

    required_fields = ["date", "category", "amount", "description"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return error(f"Missing fields: {', '.join(missing)}", 400)

    date = str(data.get("date", "")).strip()
    category = str(data.get("category", "")).strip()
    description = str(data.get("description", "")).strip()

    # amount can be int/float/string -> convert safely
    try:
        amount = float(data.get("amount"))
    except (TypeError, ValueError):
        return error("Amount must be a number.", 400)

    if not date or not is_valid_date(date):
        return error("Date must be in YYYY-MM-DD format.", 400)

    if not category:
        return error("Category cannot be empty.", 400)

    if amount <= 0:
        return error("Amount must be greater than 0.", 400)

    if len(description) == 0:
        return error("Description cannot be empty.", 400)

    exp = Expense(date=date, category=category, amount=amount, description=description)
    db.session.add(exp)
    db.session.commit()

    return jsonify({"message": "Expense added successfully.", "expense": exp.to_dict()}), 201


@app.route("/expenses", methods=["GET"])
def get_expenses():
    expenses = Expense.query.order_by(Expense.id.desc()).all()
    return jsonify({
        "count": len(expenses),
        "expenses": [e.to_dict() for e in expenses]
    }), 200


@app.route("/expenses/summary", methods=["GET"])
def summary():
    total = db.session.query(func.coalesce(func.sum(Expense.amount), 0.0)).scalar()

    breakdown_rows = (
        db.session.query(Expense.category, func.sum(Expense.amount))
        .group_by(Expense.category)
        .all()
    )
    category_breakdown = [
        {"category": cat, "total": float(cat_total)} for cat, cat_total in breakdown_rows
    ]

    highest = None
    if category_breakdown:
        highest = max(category_breakdown, key=lambda x: x["total"])

    return jsonify({
        "total_spending": float(total),
        "category_breakdown": category_breakdown,
        "highest_spending_category": highest  # null if no data
    }), 200


@app.route("/expenses/monthly", methods=["GET"])
def monthly_report():
    month = request.args.get("month")
    year = request.args.get("year")

    if not month or not year:
        return error("Query params 'month' and 'year' are required. Example: /expenses/monthly?month=2&year=2026", 400)

    try:
        month_int = int(month)
        year_int = int(year)
    except ValueError:
        return error("'month' and 'year' must be integers.", 400)

    if month_int < 1 or month_int > 12:
        return error("'month' must be between 1 and 12.", 400)

    if year_int < 1900 or year_int > 2100:
        return error("'year' must be between 1900 and 2100.", 400)

    prefix_dash = f"{year_int:04d}-{month_int:02d}-"
    prefix_slash = f"{year_int:04d}/{month_int:02d}/"

    expenses = (Expense.query
            .filter((Expense.date.like(f"{prefix_dash}%")) | (Expense.date.like(f"{prefix_slash}%")))
            .order_by(Expense.date.asc())
            .all())


    total = sum(e.amount for e in expenses)

    # category-wise
    cat_totals = {}
    for e in expenses:
        cat_totals[e.category] = cat_totals.get(e.category, 0.0) + e.amount

    category_breakdown = [{"category": k, "total": float(v)} for k, v in cat_totals.items()]
    highest = None
    if category_breakdown:
        highest = max(category_breakdown, key=lambda x: x["total"])

    return jsonify({
        "month": month_int,
        "year": year_int,
        "count": len(expenses),
        "total_spending": float(total),
        "category_breakdown": category_breakdown,
        "highest_spending_category": highest,
        "expenses": [e.to_dict() for e in expenses]
    }), 200


@app.errorhandler(404)
def not_found(_):
    return error("Route not found.", 404)


@app.errorhandler(405)
def method_not_allowed(_):
    return error("Method not allowed for this route.", 405)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
