import React from 'react';
import './MenuItem.css';

const MenuItem = ({ title, price, tags, imageUrl, onAddToCart }) => {
  return (
    <div className="app__menuitem">
      <div className="app__menuitem-head">
        <div className="app__menuitem-name">
          <p className="p__cormorant" style={{ color: '#DCCA87' }}>{title}</p>
        </div>
        <div className="app__menuitem-dash" />
        <div className="app__menuitem-price">
          <p className="p__cormorant">{price}</p>
        </div>
      </div>

      <div className="app__menuitem-sub">
        <p className="p__opensans">{tags}</p>
      </div>

      {/* ✅ Render image here */}
      {imageUrl && (
        <img
        alt={title}
          src={imageUrl}
          className="menu-item-image"
          style={{ width: '100%', height: 'auto', borderRadius: '8px', marginTop: '10px' }}
        />
      )}

      <button className="custom__button" onClick={onAddToCart}>
        Add to Cart
      </button>
    </div>
  );
};

export default MenuItem;
