import React, { useState, useEffect } from 'react';
import axios from 'axios';

function OwnerDashboard() {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [orders, setOrders] = useState([]);
  const token = localStorage.getItem('token');

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/orders', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOrders(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const addMenuItem = async (e) => {
    e.preventDefault();
    try {
      await axios.post(
        'http://localhost:8000/api/menu',
        { name, price: parseFloat(price) },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('Menu item added!');
      setName('');
      setPrice('');
    } catch (err) {
      alert('Error adding item');
    }
  };

  const updateOrderStatus = async (orderId, newStatus) => {
    try {
      await axios.put(
        `http://localhost:8000/api/orders/${orderId}/status`,
        { status: newStatus },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchOrders();
    } catch (err) {
      alert('Failed to update status');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Restaurant Owner Dashboard</h2>
      <form onSubmit={addMenuItem} style={{ marginBottom: '30px' }}>
        <h3>Add New Dish</h3>
        <input type="text" placeholder="Dish Name" value={name} onChange={(e) => setName(e.target.value)} required style={{ marginRight: '10px', padding: '6px' }} />
        <input type="number" placeholder="Price" value={price} onChange={(e) => setPrice(e.target.value)} required style={{ marginRight: '10px', padding: '6px' }} />
        <button type="submit" style={{ padding: '6px 15px', backgroundColor: '#007bff', color: 'white', border: 'none' }}>Add Item</button>
      </form>

      <h3>Incoming Orders</h3>
      {orders.map((order) => (
        <div key={order.id} style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '10px' }}>
          <p>Order #{order.id}: {order.item_name} | Current Status: <strong>{order.status}</strong></p>
          <button onClick={() => updateOrderStatus(order.id, 'Preparing')} style={{ marginRight: '10px' }}>Mark Preparing</button>
          <button onClick={() => updateOrderStatus(order.id, 'Ready for Pickup')}>Ready for Pickup</button>
        </div>
      ))}
    </div>
  );
}

export default OwnerDashboard;