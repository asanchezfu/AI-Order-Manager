from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse
from backend.services import order_service, llm_service
from backend.database import Base, engine, SessionLocal
from backend.models import order

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tenis Pro Orders API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "Backend is running 🚀"}

@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, order)

@app.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: str, update: OrderUpdate, db: Session = Depends(get_db)):
    updated = order_service.update_order_state(db, order_id, update.order_state)

    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")

    # 👀 Trigger LLM notification if status == "Despachado"
    if updated.order_state.lower() == "Despachado":
        msg = llm_service.generate_notification(updated)
        print("\n📧 Notification Draft:\n", msg, "\n")

    return updated

# 3️⃣ List all Orders
@app.get("/orders", response_model=list[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return order_service.get_orders(db)
