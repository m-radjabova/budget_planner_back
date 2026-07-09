import uuid
from datetime import date, timedelta
from sqlalchemy import delete, select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.budget import Budget
from app.models.category import Category
from app.models.debt import Debt
from app.models.enums import DebtStatus, EntryType, NotificationType, RecurringFrequency, UserRole
from app.models.note import Note
from app.models.notification import Notification
from app.models.recurring_transaction import RecurringTransaction
from app.models.savings_goal import SavingsGoal
from app.models.transaction import Transaction
from app.models.user import User

DEMO_USER_ID = uuid.UUID("0f9edaeb-76e3-4435-9e4f-be1964417c97")
DEMO_EMAIL = "demo@budgetplanner.com"
DEMO_PASSWORD = "demo12345"


def seed_admin(db):
    admin = db.scalar(select(User).where(User.email == "admin@budgetplanner.com"))
    if admin:
        return

    db.add(
        User(
            full_name="Admin User",
            email="admin@budgetplanner.com",
            hashed_password=hash_password("admin123"),
            role=UserRole.ADMIN,
            currency="USD",
        )
    )
    db.commit()


def seed_demo_user(db):
    demo_user = db.get(User, DEMO_USER_ID)
    if demo_user is None:
        demo_user = User(
            id=DEMO_USER_ID,
            full_name="Budget Demo User",
            email=DEMO_EMAIL,
            hashed_password=hash_password(DEMO_PASSWORD),
            role=UserRole.USER,
            currency="USD",
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
    else:
        demo_user.full_name = "Budget Demo User"
        demo_user.email = DEMO_EMAIL
        demo_user.hashed_password = hash_password(DEMO_PASSWORD)
        demo_user.role = UserRole.USER
        demo_user.currency = "USD"
        db.commit()

    for model in [Notification, RecurringTransaction, Note, Debt, SavingsGoal, Budget, Transaction, Category]:
        db.execute(delete(model).where(model.user_id == DEMO_USER_ID))
    db.commit()

    today = date.today()
    first_day = today.replace(day=1)

    categories = {
        "Salary": Category(user_id=DEMO_USER_ID, name="Salary", icon="briefcase", color="#22c55e", type=EntryType.INCOME),
        "Freelance": Category(user_id=DEMO_USER_ID, name="Freelance", icon="sparkles", color="#8b5cf6", type=EntryType.INCOME),
        "Food": Category(user_id=DEMO_USER_ID, name="Food", icon="utensils", color="#fb923c", type=EntryType.EXPENSE),
        "Housing": Category(user_id=DEMO_USER_ID, name="Housing", icon="home", color="#4f7cff", type=EntryType.EXPENSE),
        "Transportation": Category(user_id=DEMO_USER_ID, name="Transportation", icon="car", color="#facc15", type=EntryType.EXPENSE),
        "Health": Category(user_id=DEMO_USER_ID, name="Health", icon="heart", color="#ef4444", type=EntryType.EXPENSE),
    }
    db.add_all(categories.values())
    db.commit()

    transactions = [
        Transaction(user_id=DEMO_USER_ID, category_id=categories["Salary"].id, title="Monthly Salary", amount=4000, type=EntryType.INCOME, transaction_date=first_day + timedelta(days=1), description="Main monthly salary", tags=["#work", "#salary"]),
        Transaction(user_id=DEMO_USER_ID, category_id=categories["Freelance"].id, title="Freelance Payment", amount=1400, type=EntryType.INCOME, transaction_date=first_day + timedelta(days=5), description="Website project payment", tags=["#work", "#freelance"]),
        Transaction(user_id=DEMO_USER_ID, category_id=categories["Food"].id, title="Groceries", amount=220, type=EntryType.EXPENSE, transaction_date=first_day + timedelta(days=3), description="Family grocery shopping", tags=["#family", "#food"]),
        Transaction(user_id=DEMO_USER_ID, category_id=categories["Food"].id, title="Restaurant Dinner", amount=140, type=EntryType.EXPENSE, transaction_date=first_day + timedelta(days=7), description="Dinner with family", tags=["#family", "#food"]),
        Transaction(user_id=DEMO_USER_ID, category_id=categories["Food"].id, title="Weekly Market", amount=120, type=EntryType.EXPENSE, transaction_date=first_day + timedelta(days=10), description="Fresh food and fruit", tags=["#food", "#health"]),
        Transaction(user_id=DEMO_USER_ID, category_id=categories["Housing"].id, title="Apartment Rent", amount=850, type=EntryType.EXPENSE, transaction_date=first_day + timedelta(days=2), description="Monthly rent", tags=["#family", "#home"]),
        Transaction(user_id=DEMO_USER_ID, category_id=categories["Transportation"].id, title="Fuel", amount=90, type=EntryType.EXPENSE, transaction_date=first_day + timedelta(days=9), description="Car fuel refill", tags=["#travel"]),
        Transaction(user_id=DEMO_USER_ID, category_id=categories["Health"].id, title="Pharmacy", amount=65, type=EntryType.EXPENSE, transaction_date=first_day + timedelta(days=11), description="Health essentials", tags=["#health"]),
    ]
    db.add_all(transactions)

    budgets = [
        Budget(user_id=DEMO_USER_ID, category_id=categories["Food"].id, month=today.month, year=today.year, limit_amount=500),
        Budget(user_id=DEMO_USER_ID, category_id=categories["Housing"].id, month=today.month, year=today.year, limit_amount=1000),
        Budget(user_id=DEMO_USER_ID, category_id=categories["Transportation"].id, month=today.month, year=today.year, limit_amount=300),
        Budget(user_id=DEMO_USER_ID, category_id=categories["Health"].id, month=today.month, year=today.year, limit_amount=250),
    ]
    db.add_all(budgets)

    db.add_all([
        SavingsGoal(user_id=DEMO_USER_ID, title="Vacation Trip", target_amount=2000, current_amount=1200, deadline=today + timedelta(days=120), icon="sun", color="#8b5cf6"),
        SavingsGoal(user_id=DEMO_USER_ID, title="Emergency Fund", target_amount=3000, current_amount=1000, deadline=today + timedelta(days=200), icon="shield", color="#22c55e"),
    ])

    db.add_all([
        Debt(user_id=DEMO_USER_ID, title="Credit Card", total_amount=2500, paid_amount=1200, minimum_payment=150, due_date=today + timedelta(days=12), status=DebtStatus.ACTIVE),
        Debt(user_id=DEMO_USER_ID, title="Student Loan", total_amount=6000, paid_amount=3500, minimum_payment=220, due_date=today + timedelta(days=20), status=DebtStatus.ACTIVE),
    ])

    db.add_all([
        Note(user_id=DEMO_USER_ID, title="Review insurance plan", content="Check new offer before the 15th.", note_date=today + timedelta(days=5)),
        Note(user_id=DEMO_USER_ID, title="Plan family trip", content="Compare hotel costs and travel budget.", note_date=today + timedelta(days=9)),
    ])

    db.add_all([
        RecurringTransaction(user_id=DEMO_USER_ID, category_id=categories["Salary"].id, title="Monthly Salary", amount=4000, type=EntryType.INCOME, frequency=RecurringFrequency.MONTHLY, start_date=first_day, is_active=True),
        RecurringTransaction(user_id=DEMO_USER_ID, category_id=categories["Housing"].id, title="Rent", amount=850, type=EntryType.EXPENSE, frequency=RecurringFrequency.MONTHLY, start_date=first_day, is_active=True),
    ])

    db.add_all([
        Notification(user_id=DEMO_USER_ID, title="Budget Alert: Food", message="You have used 96% of your Food budget.", type=NotificationType.BUDGET, is_read=False),
        Notification(user_id=DEMO_USER_ID, title="Welcome back", message="Your demo workspace is ready with budgets, tags, analytics and alerts.", type=NotificationType.SYSTEM, is_read=False),
    ])

    db.commit()
    print(f"Demo user seeded: {DEMO_EMAIL} / {DEMO_PASSWORD}")


def main():
    db = SessionLocal()
    try:
        seed_admin(db)
        seed_demo_user(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
