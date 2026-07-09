from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers.auth import router as auth_router
from app.routers.budgets import router as budget_router
from app.routers.categories import router as category_router
from app.routers.debts import router as debt_router
from app.routers.notes import router as note_router
from app.routers.notifications import router as notification_router
from app.routers.recurring_transactions import router as recurring_router
from app.routers.savings_goals import router as savings_goal_router
from app.routers.transactions import router as transaction_router
from app.routers.users import router as user_router

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(transaction_router)
app.include_router(budget_router)
app.include_router(savings_goal_router)
app.include_router(debt_router)
app.include_router(note_router)
app.include_router(recurring_router)
app.include_router(notification_router)


@app.get("/health", tags=["Health"])
def healthcheck():
    return {"status": "ok"}
