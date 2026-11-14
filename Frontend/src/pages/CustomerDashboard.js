import React, { useState, useEffect } from 'react';
import axios from 'axios';

function CustomerDashboard() {
  const [menuItems, setMenuItems] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [cart, setCart] = useState([]);
  const [aiSummary, setAiSummary] = useState(""); 
  const [orders, setOrders] = useState([]);
  const [restaurants, setRestaurants] = useState([]);
  const token = localStorage.getItem('token');

  useEffect(() => {
    fetchMenu();
    fetchRestaurants();
    fetchOrders();
  }, []);

  const fetchMenu = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/menu');
      setMenuItems(res.data);
    } catch (err) {
      console.error('Error fetching menu', err);
    }
  };

  const fetchRestaurants = async () => {
     try {
       const res = await axios.get('http://localhost:8000/api/restaurants');
       setRestaurants(res.data);
     } catch (err) {
       console.error('Error fetching restaurants', err);
     }
   };
   
   const fetchOrders = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/orders', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOrders(res.data);
    } catch (err) {
      console.error('Error fetching orders', err);
    }
  };

  const placeOrder = async (item) => {
    try {
      await axios.post(
        'http://localhost:8000/api/orders',
        { item_name: item.name, total_price: item.price },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert(`Order placed for ${item.name}!`);
      fetchOrders();
    } catch (err) {
      alert('Failed to place order');
    }
  };
    
    // Search & Filter (Point 4)
const filteredMenu = menuItems.filter(item =>
  item.name.toLowerCase().includes(searchQuery.toLowerCase())
);

// Add to Cart (Point 5)
const addToCart = (item) => {
  setCart([...cart, item]);
  alert(`${item.name} added to cart!`);
};

// Cancel Order (Point 10)
const cancelOrder = async (orderId) => {
  await fetch(`http://127.0.0.1:8000/orders/${orderId}/cancel`, { method: 'PATCH' });
  alert("Order Cancelled!");
  // यहाँ orders को दुबारा fetch करने का फंक्शन कॉल करें
};

  return (
    <div style={{ padding: '20px' }}>
      <h2>Customer Dashboard - CampusBite</h2>
      {/* Search Bar (Point 4) */}
<input 
  type="text" 
  placeholder="Search dishes..." 
  value={searchQuery}
  onChange={(e) => setSearchQuery(e.target.value)}
  style={{ padding: '8px', marginBottom: '15px', width: '300px' }}
/>

{/* Cart Section (Point 5 & 6) */}
<div style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '20px' }}>
  <h4>Your Cart ({cart.length} items)</h4>
  {cart.map((c, index) => <p key={index}>{c.name} - ₹{c.price}</p>)}
</div>
      <h3>Available Menu</h3>
      <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap' }}>
        {filteredMenu.map((item) => (
          <div key={item.id} style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '8px', width: '200px' }}>
            <h4>{item.name}</h4>
            <p>Price: ₹{item.price}</p>
            <button onClick={() => placeOrder(item)} style={{ padding: '6px 12px', backgroundColor: '#28a745', color: 'white', border: 'none' }}>
              Order Now
            </button>
          </div>
        ))}
      </div>
      <h3 style={{ marginTop: '20px' }}>Available Restaurants</h3>
      <div style={{ display: 'flex', gap: '15px', marginBottom: '25px', flexWrap: 'wrap' }}>
         {restaurants.map((rest) => (
           <div key={rest.id} style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '8px', width: '220px', background: '#f9f9f9' }}>
             <h4>{rest.name}</h4>
             <p>{rest.location || 'Campus Area'}</p>
           </div>
      ))}
      </div>

      <h3 style={{ marginTop: '30px' }}>My Orders</h3>
      <ul>
        {orders.map((order) => (
          <li key={order.id}>
            Order #{order.id} - {order.item_name} - <strong>Status: {order.status}</strong>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CustomerDashboard;