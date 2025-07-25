import React from 'react';
import './Cart.css';

const Cart = ({ items, onRemove, onAdd, onRemoveCompletely }) => {
  const totalCost = items.reduce(
    (total, item) => total + item.price * item.quantity,
    0
  );

  return (
    <div className="cart app__specialMenu flex__center section__padding slide-bottom">
      <h2 className="headtext__cormorant" style={{ color: '#DCCA87' }}>Your Cart</h2>

      {items.length === 0 && (
        <p className="p__opensans" style={{ color: '#AAA' }}>Your cart is empty.</p>
      )}

      {items.map((item) => (
        <div key={item.id} className="cart-item">
          <div className="cart-item-info">
            <p className="p__cormorant" style={{ color: '#dcca87' }}>{item.name}</p>
            <p className="p__opensans" style={{ color: '#AAA' }}>Rs. {item.price}</p>
          </div>

          <div className="quantity-controls">
            <button className="quantity-btn" onClick={() => onRemove(item.id)}>-</button>
            <span className="p__opensans" style={{ color: '#DCCA87', margin: '0 10px' }}>{item.quantity}</span>
            <button className="quantity-btn" onClick={() => onAdd(item)}>+</button>
          </div>

          <p className="p__opensans" style={{ color: '#AAA', minWidth: '80px', textAlign: 'right' }}>
            Rs. {item.price * item.quantity}
          </p>

          <button
            className="remove-btn p__opensans"
            onClick={() => onRemoveCompletely(item.id)}
          >
            Remove
          </button>
        </div>
      ))}

      {items.length > 0 && (
        <>
          <h3 className="headtext__cormorant" style={{ color: '#DCCA87', marginTop: 20 }}>
            Total: Rs. {totalCost}
          </h3>
          <button className="custom__button" style={{ marginTop: 15 }}>
            Checkout
          </button>
        </>
      )}
    </div>
  );
};


export default Cart;
