from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta

# Local application imports
import models
from .import schemas
from .import database
from .import auth

# Database tables create karna
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# CORS Middleware setup taaki frontend (localhost:3000 ya 3001) connect ho sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "CampusBite Backend is running successfully!"}

# --- REGISTER ENDPOINT ---
@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and create user
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- LOGIN ENDPOINT ---
@app.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    

    return {
        "message": "Login successful",
        "access_token": auth.create_access_token(data={"sub": db_user.email}),
        "token_type": "bearer",
        "role": db_user.role
    }
from fastapi.middleware.cors import CORSMiddleware
# Restaurant List Fetch Karne Ka Route
@app.get("/restaurants")
@app.get("/api/restaurants")
def get_restaurants(db: Session = Depends(get_db)):
    # Maan lijiye aapne models.Restaurant banaya hai
    return db.query(models.Restaurant).all()

@app.get("/api/menu", response_model=list[schemas.MenuItemResponse])
def get_menu(db: Session = Depends(get_db)):
    # Sabhi available dishes fetch karega
    return db.query(models.MenuItem).filter(models.MenuItem.is_available == 1).all()

@app.post("/api/menu")
def add_menu_item(item: dict, db: Session = Depends(get_db)):
    # Frontend se aane wale data ko direct database model mein daal rahe hain
    db_item = models.MenuItem(
        name=item.get("name"),
        price=float(item.get("price", 0)),
        restaurant_id=int(item.get("restaurant_id", 1)),
        is_available=int(item.get("is_available", 1))
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.post("/api/orders", response_model=schemas.OrderResponse)
def place_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    total = 0.0
    # Total price calculate karein
    for item in order.items:
        menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == item.menu_item_id).first()
        if menu_item:
          total += menu_item.price * item.quantity

    # Order create karein
    new_order = models.Order(
        customer_id=1,  # Authenticated user ID yahan pass kar sakte hain
        restaurant_id=order.restaurant_id,
        total_price=total,
        status="PLACED",
        payment_status="MOCK_PAID"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Order items save karein
    for item in order.items:
        order_item = models.OrderItem(
            order_id=new_order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity
        )
        db.add(order_item)
    db.commit()

    return new_order

@app.patch("/api/orders/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status  # Jaise: PREPARING, OUT_FOR_DELIVERY, DELIVERED
    db.commit()
    db.refresh(order)
    return {"message": "Order status updated successfully", "new_status": order.status}
# 1. Restaurants list fetch karne ke liye (Agar Restaurant table nahi hai toh dummy list bhejega)
@app.get("/restaurants")
@app.get("/api/restaurants")
def get_restaurants(db: Session = Depends(get_db)):
    try:
        restaurants = db.query(models.Restaurant).all()
        if restaurants:
            return restaurants
    except Exception:
        pass
    # Agar database mein Restaurant model/data abhi nahi hai toh ye default dikhega
    return [
        {"id": 1, "name": "Campus Canteen", "location": "Main Block"},
        {"id": 2, "name": "Nescafe Corner", "location": "Library Gate"}
    ]

# 2. Orders list fetch karne ke liye (405 error hatane ke liye)
@app.get("/orders")
@app.get("/api/orders")
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

# 10. Order Cancel करने के लिए
@app.patch("/orders/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "Pending":
        raise HTTPException(status_code=400, detail="Cannot cancel order now")
    order.status = "Cancelled"
    db.commit()
    return {"message": "Order cancelled successfully"}

# 11. Rating & Review सबमिट करने के लिए
@app.post("/reviews/")
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    new_review = models.Review(**review.dict())
    db.add(new_review)
    db.commit()
    return {"message": "Review submitted"}

# 12. Refund Request के लिए
@app.patch("/orders/{order_id}/refund")
def request_refund(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order and order.status == "Delivered":
        order.refund_requested = True
        db.commit()
        return {"message": "Refund requested"}
    raise HTTPException(status_code=400, detail="Refund only allowed after delivery")

# 13. AI-Generated Order Summary के लिए
@app.get("/orders/ai-summary/{user_id}")
def get_ai_summary(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.user_id == user_id).all()
    if not orders:
        return {"summary": "You haven't placed any orders yet. Try ordering Aloo Paratha!"}
    total_orders = len(orders)
    return {
        "summary": f"AI Insight: You have placed {total_orders} orders so far. Your ordering trend shows a strong preference for quick campus snacks!"
    }