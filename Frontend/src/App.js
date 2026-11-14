import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import CustomerDashboard from './pages/CustomerDashboard';
import OwnerDashboard from './pages/OwnerDashboard';
import DeliveryDashboard from './pages/DeliveryDashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/customer" element={<CustomerDashboard />} />
        <Route path="/owner" element={<OwnerDashboard />} />
        <Route path="/delivery" element={<DeliveryDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;