// src/pages/OrderHistoryPage.js

import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './OrderHistoryPage.css'; // We will create this CSS file

const OrderHistoryPage = () => {
  const { authTokens } = useContext(AuthContext);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/orders/', {
          headers: { 'Authorization': `Bearer ${authTokens.access}` }
        });
        if (!response.ok) throw new Error("Could not fetch order history.");
        const data = await response.json();
        setOrders(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (authTokens) {
      fetchOrders();
    }
  }, [authTokens]);

  if (loading) return <div className="order-history-container"><p className="p__opensans">Loading Order History...</p></div>;
  if (error) return <div className="order-history-container"><p className="p__cormorant" style={{color: 'red'}}>{error}</p></div>;

  return (
    <div className="order-history-container section__padding">
      <h1 className="headtext__cormorant">My Order History</h1>
      
      {orders.length === 0 ? (
        <p className="p__opensans">You have not placed any orders yet.</p>
      ) : (
        <ul className="orders-list">
          {orders.map(order => (
            <li key={order.id} className="order-item">
              <div className="order-item-info">
                <span className="p__cormorant">Order #{order.id}</span>
                <span className="p__opensans">Date: {new Date(order.created_at).toLocaleDateString()}</span>
                <span className="p__opensans">Total: Rs. {order.total_price}</span>
              </div>
              <Link to={`/order/${order.id}`} className="custom__button">
                View Receipt
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default OrderHistoryPage;