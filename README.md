# Personal Expense Analyzer API (Flask + SQLite)

A Python REST API to add, retrieve, and analyze personal expense data.

---

## Features
- Add a new expense (POST)
- Retrieve all expenses (GET)
- Summary report:
  - Total spending
  - Category-wise totals
  - Highest spending category
- Monthly report by month & year

---

## Tech Stack
- Python
- Flask
- SQLite
- SQLAlchemy (ORM)

---

## Setup & Run

### 1) Clone repository
```bash
git clone <your-repo-url>
cd personal-expense-analyzer-api
```

### 2) Create Virtual Environment
```bash
python -m venv venv
```

Activate it:

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

### 3) Install Dependencies
```bash
pip install -r requirements.txt
```

### 4) Run the Application
```bash
python app.py
```

Server runs at:
```
http://127.0.0.1:5000
```

---

# API Endpoints

## 1) Health Check
**GET** `/health`

Response:
```json
{
  "status": "ok"
}
```

---

## 2) Add Expense
**POST** `/expenses`

Request Body:
```json
{
  "date": "2026-02-14",
  "category": "food",
  "amount": 120.50,
  "description": "Dinner"
}
```

Success Response:
```json
{
  "message": "Expense added successfully.",
  "expense": {
    "id": 1,
    "date": "2026-02-14",
    "category": "food",
    "amount": 120.5,
    "description": "Dinner"
  }
}
```

---

## 3) Get All Expenses
**GET** `/expenses`

Response:
```json
{
  "count": 2,
  "expenses": [
    {
      "id": 1,
      "date": "2026-02-14",
      "category": "food",
      "amount": 120.5,
      "description": "Dinner"
    }
  ]
}
```

---

## 4) Summary Report
**GET** `/expenses/summary`

Response:
```json
{
  "total_spending": 180.5,
  "category_breakdown": [
    { "category": "food", "total": 120.5 },
    { "category": "transport", "total": 60.0 }
  ],
  "highest_spending_category": {
    "category": "food",
    "total": 120.5
  }
}
```

---

## 5) Monthly Report
**GET** `/expenses/monthly?month=2&year=2026`

Response:
```json
{
  "month": 2,
  "year": 2026,
  "count": 2,
  "total_spending": 180.5,
  "category_breakdown": [
    { "category": "food", "total": 120.5 },
    { "category": "transport", "total": 60.0 }
  ],
  "highest_spending_category": {
    "category": "food",
    "total": 120.5
  },
  "expenses": [
    {
      "id": 1,
      "date": "2026-02-14",
      "category": "food",
      "amount": 120.5,
      "description": "Dinner"
    }
  ]
}
```

---

## Validation & Error Handling

The API validates:
- Required fields must be present
- Date format must be `YYYY-MM-DD`
- Amount must be numeric and greater than 0
- Month must be between 1 and 12
- Year must be between 1900 and 2100

Error response format:
```json
{
  "error": "Error message"
}
```

---

## Example cURL Command

Add expense:
```bash
curl -X POST http://127.0.0.1:5000/expenses \
  -H "Content-Type: application/json" \
  -d '{"date":"2026-02-14","category":"food","amount":120.5,"description":"Dinner"}'
```

---

## Future Improvements
- Add update and delete endpoints
- Add authentication
- Add pagination
- Deploy to cloud

Explanation video:https://www.youtube.com/watch?v=OpIgAfVXH6I
Images of Project Execution:
<img width="1612" height="956" alt="Screenshot 2026-02-15 185251" src="https://github.com/user-attachments/assets/a0b1107b-e4a7-4d0c-8de6-a881a80e48dd" />
<img width="1622" height="1006" alt="Screenshot 2026-02-15 185208" src="https://github.com/user-attachments/assets/2525cfb4-fef5-4e3f-9f3e-e8ac4006a21d" />
<img width="1919" height="1017" alt="Screenshot 2026-02-14 220102" src="https://github.com/user-attachments/assets/53c6fdab-b79a-4671-a4ff-d2cfa1a909e6" />
<img width="1919" height="1022" alt="Screenshot 2026-02-14 215910" src="https://github.com/user-attachments/assets/1602a640-3b66-45ff-bb72-8174d9954040" />


