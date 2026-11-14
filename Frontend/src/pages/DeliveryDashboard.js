import React, { useState, useEffect } from 'react';
import axios from 'axios';

function DeliveryDashboard() {
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

  const updateStatus = async (orderId, status) => {
    try {
      await axios.put(
        `http://localhost:8000/api/orders/${orderId}/status`,
        { status },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchOrders();
    } catch (err) {
      alert('Error updating delivery status');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Delivery Partner Dashboard</h2>
      {orders.map((order) => (
        <div key={order.id} style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '10px' }}>
          <p>Order #{order.id} - {order.item_name} | Status: <strong>{order.status}</strong></p>
          <button onClick={() => updateStatus(order.id, 'Out for Delivery')} style={{ marginRight: '10px' }}>Out for Delivery</button>
          <button onClick={() => updateStatus(order.id, 'Delivered')} style={{ backgroundColor: '#28a745', color: 'white', border: 'none', padding: '5px 10px' }}>Mark Delivered</button>
        </div>
      ))}
    </div>
  );
}

export default DeliveryDashboard;