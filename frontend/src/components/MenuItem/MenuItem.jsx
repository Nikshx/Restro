import React from 'react';
import './MenuItem.css';

const MenuItem = ({ title, price, tags, imageUrl, onAddToCart }) => {
  return (
    <div className="app__menuitem">
      {/* Add image here */}
      {imageUrl && (
        <div className="app__menuitem-img">
          <img src={imageUrl} alt={title} style={{ width: '100%', maxHeight: '200px', objectFit: 'cover' }} />
        </div>
      )}

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
        <p className="p__opensans" style={{ color: '#AAAAAA' }}>{tags}</p>

        <button type="button" className="custom__button" onClick={onAddToCart} style={{ marginTop: '1rem' }}>
          Add to Cart
        </button>
      </div>
    </div>
  );
};

export default MenuItem;
