import React, { useEffect, useState } from 'react';
import { SubHeading, MenuItem } from '../../components';
import './CanteenMenu.css';
import images from '../../constants/images'; 
import Cart from '../Cart/Cart';

const CanteenMenu = () => {
  const [foods, setFoods] = useState([]);
  const [drinks, setDrinks] = useState([]);
  const [cartItems, setCartItems] = useState([]);
  const [isCartVisible, setIsCartVisible] = useState(false);


useEffect(() => {
  const token = localStorage.getItem("token");

  fetch("http://localhost:8000/api/menu-item/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    }
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }
      return res.json();
    })
    .then((data) => {
      const foodItems = data.filter(item => item.category === "food");
      const drinkItems = data.filter(item => item.category === "drink");
      setFoods(foodItems);
      setDrinks(drinkItems);
    })
    .catch((err) => console.error("Fetch menu error:", err));
}, []);


  // Add item to cart or increase quantity if already in cart
  const addToCart = (item) => {
    setCartItems(prevItems => {
      const exist = prevItems.find(cartItem => cartItem.id === item.id);
      if (exist) {
        return prevItems.map(cartItem =>
          cartItem.id === item.id 
            ? { ...cartItem, quantity: cartItem.quantity + 1 } 
            : cartItem
        );
      }
      return [...prevItems, { ...item, quantity: 1 }];
    });
  };

  const removeFromCart = (item) => {
  setCartItems((prevItems) => {
    const existingItem = prevItems.find((i) => i.id === item.id);
    if (!existingItem) return prevItems;

    if (existingItem.quantity === 1) {
      return prevItems.filter((i) => i.id !== item.id);
    } else {
      return prevItems.map((i) =>
        i.id === item.id ? { ...i, quantity: i.quantity - 1 } : i
      );
    }
  });
};


  return (
    <div className="app__specialMenu flex__center section__padding" id="menu">
      <div className="app__specialMenu-title">
        <SubHeading title="Menu that fits your palate" />
        <h1 className="headtext__cormorant">Today's Special</h1>
      </div>

      <div className="app__specialMenu-menu">
        <div className="app__specialMenu-menu_wine flex__center">
          <p className="app__specialMenu-menu_heading">Foods</p>
          <div className="app__specialMenu_menu_items">
            {foods.map((item, index) => (
              <MenuItem
                key={item.name + index}
                title={item.name}
                price={`Rs. ${item.price}`}
                tags={item.description || "No description"}
                imageUrl={item.image_url}
                onAddToCart={() => addToCart(item)}
              />
            ))}
          </div>
        </div>

        <div className="app__specialMenu-menu_img">
          <img src={images.menu} alt="menu" />
        </div>

        <div className="app__specialMenu-menu_cocktails flex__center">
          <p className="app__specialMenu-menu_heading">Drinks</p>
          <div className="app__specialMenu_menu_items">
            {drinks.map((item, index) => (
              <MenuItem
                key={item.name + index}
                title={item.name}
                price={`Rs. ${item.price}`}
                tags={item.description || "No description"}
                imageUrl={item.image_url}
                onAddToCart={() => addToCart(item)}
              />
            ))}
          </div>
        </div>
      </div>

<div style={{ marginTop: 15 }}>
  <button onClick={() => setIsCartVisible(!isCartVisible)} className="custom__button">
    {isCartVisible ? 'Hide Cart' : 'View Cart'}
  </button>

  {isCartVisible && (
    <Cart items={cartItems} onRemove={removeFromCart} onAdd={addToCart} />
  )}
</div>
    </div>
  );
};

export default CanteenMenu;
