# 🍔 CampusBite - Smart Campus Food Ordering System

CampusBite is a full-stack web application designed for campus food ordering, featuring multi-user roles, real-time tracking, AI-powered order insights, and complete containerization via Docker.

---

## 🚀 Tech Stack

* **Frontend:** React.js, HTML5, CSS3, JavaScript
* **Backend:** Python, FastAPI, SQLAlchemy
* **Database:** SQLite / Relational SQL Database
* **Containerization:** Docker, Docker Compose

---

## ✨ Key Features & Functionalities

1. **User Authentication & Authorization:** Secure login and role-based access for Customers, Restaurant Owners, and Delivery Partners.
2. **Interactive Menu Management:** Browse pure vegetarian and fast-food items (like Aloo Paratha, Punjabi Lassi, Maggi, Pasta), managed by restaurant owners.
3. **Advanced Search & Filter:** Quickly find your favorite meals.
4. **Shopping Cart & Checkout:** Seamless item addition, removal, and order placement.
5. **Order Tracking & Cancellation:** Real-time order status updates and cancellation support for pending orders.
6. **Ratings & Reviews:** Submit ratings and comments for completed orders.
7. **Refund & Return Requests:** Manage return/refund workflows seamlessly.
8. **AI-Powered Order Insights:** Customers can access AI-generated summaries and analytics based on their order history.
9. **Docker Support:** Fully containerized setup for effortless deployment.

---

## 📂 Project Structure

```text
CampusBite/
│
├── Backend/
│   ├── Application/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── schemas.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── Frontend/
│   ├── src/
│   │   ├── pages/
│   │   └── App.js
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
└── README.md