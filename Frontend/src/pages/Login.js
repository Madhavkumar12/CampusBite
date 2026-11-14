import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('customer');
  const [isRegister, setIsRegister] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const endpoint = isRegister ? 'http://localhost:8000/register' : 'http://localhost:8000/login';
      const response = await axios.post(endpoint, {
        email,
        password,
        role
      });

      if (!isRegister) {
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('role', response.data.role || role);
        const userRole = response.data.role || role;
        if (userRole === 'customer') navigate('/customer');
        else if (userRole === 'owner') navigate('/owner');
        else if (userRole === 'delivery') navigate('/delivery');
      } else {
        alert('Registration successful! Please login now.');
        setIsRegister(false);
      }
    } catch (err) {
      alert(err.response?.data?.detail || 'Authentication failed! Check backend connection.');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>CampusBite - {isRegister ? 'Register' : 'Login'}</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label>Email:</label>
          <input 
            type="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label>Password:</label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label>Select Role:</label>
          <select 
            value={role} 
            onChange={(e) => setRole(e.target.value)} 
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          >
            <option value="customer">Customer</option>
            <option value="owner">Restaurant Owner</option>
            <option value="delivery">Delivery Partner</option>
          </select>
        </div>
        <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#ff5722', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          {isRegister ? 'Sign Up' : 'Login'}
        </button>
      </form>
      <p style={{ marginTop: '15px', textAlign: 'center', cursor: 'pointer', color: 'blue' }} onClick={() => setIsRegister(!isRegister)}>
        {isRegister ? 'Already have an account? Login' : "Don't have an account? Register"}
      </p>
    </div>
  );
}

export default Login;