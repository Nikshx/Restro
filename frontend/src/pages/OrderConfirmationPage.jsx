// src/pages/OrderConfirmationPage.js (new file)

import React, { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './OrderConfirmationPage.css'; // Create this CSS file

const OrderConfirmationPage = () => {
  const { orderId } = useParams(); // Gets the ID from the URL (e.g., /order/17)
  const { authTokens } = useContext(AuthContext);
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/orders/${orderId}/`, {
          headers: { 'Authorization': `Bearer ${authTokens.access}` }
        });
        if (!response.ok) throw new Error("Failed to fetch order details.");
        const data = await response.json();
        setOrder(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (authTokens) {
      fetchOrder();
    }
  }, [orderId, authTokens]);

  if (loading) return <p className="p__opensans" style={{color: 'white', textAlign: 'center'}}>Loading Your Receipt...</p>;
  if (!order) return <p className="p__opensans" style={{color: 'white', textAlign: 'center'}}>Order not found.</p>;

  return (
    <div className="receipt__container section__padding">
      <h1 className="headtext__cormorant">Order Confirmed!</h1>
      <p className="p__opensans">Thank you for your order.</p>
      
      <div className="receipt__details">
        <h2 className="p__cormorant">Receipt for Order #{order.id}</h2>
        <p className="p__opensans">Date: {new Date(order.created_at).toLocaleString()}</p>
        
        <ul className="receipt__items-list">
          {order.items.map(item => (
            <li key={item.id} className="receipt__item">
              <span>{item.quantity} x {item.menu_item.name}</span>
              <span>Rs. {(item.price_at_purchase * item.quantity).toFixed(2)}</span>
            </li>
          ))}
        </ul>
        
        <div className="receipt__total">
          <span className="p__cormorant">Total</span>
          <span className="p__cormorant">Rs. {order.total_price}</span>
        </div>
      </div>
    </div>
  );
};

export default OrderConfirmationPage;