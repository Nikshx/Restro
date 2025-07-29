import React, { useEffect, useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { SubHeading, MenuItem } from '../../components';
import './CanteenMenu.css';
import images from '../../constants/images'; 
import Cart from '../Cart/Cart';
import { AuthContext } from '../../context/AuthContext';

const CanteenMenu = () => {
  const [foods, setFoods] = useState([]);
  const [drinks, setDrinks] = useState([]);
  const [cartItems, setCartItems] = useState([]);
  const [isCartVisible, setIsCartVisible] = useState(false);
  const { authTokens } = useContext(AuthContext);
  const navigate = useNavigate();

  
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

  const removeFromCart = (itemId) => {
    setCartItems((prevItems) => {
      const existingItem = prevItems.find((i) => i.id === itemId);
      if (existingItem?.quantity === 1) {
        return prevItems.filter((i) => i.id !== itemId);
      } 
      return prevItems.map((i) =>
        i.id === itemId ? { ...i, quantity: i.quantity - 1 } : i
      );
    });
  };

  const removeCompletelyFromCart = (itemId) => {
    setCartItems((prevItems) => prevItems.filter((i) => i.id !== itemId));
  };

  const handleCheckout = async () => {
    if (cartItems.length === 0) {
      alert("Your cart is empty and cannot be checked out.");
      return;
    }
    if (!authTokens) {
      alert("Please log in to place an order.");
      navigate('/auth');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/orders/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authTokens.access}`,
        },
        body: JSON.stringify({ cart: cartItems }),
      });

      const newOrder = await response.json();

      if (!response.ok) {
        throw new Error(newOrder.error || "An unknown error occurred during checkout.");
      }

      alert("Order placed successfully!");
      setCartItems([]);
      setIsCartVisible(false);
      navigate(`/order/${newOrder.id}`);

    } catch (err) {
      console.error("Checkout error:", err);
      alert(`Checkout Failed: ${err.message}`);
    }
  };
  
  useEffect(() => {
    const fetchMenuItems = async () => {
      const headers = { "Content-Type": "application/json" };
      if (authTokens) {
        headers["Authorization"] = `Bearer ${authTokens.access}`;
      }
      try {
        const response = await fetch("/api/menu-items/", { headers });
        const data = await response.json();
        if (!response.ok) throw new Error("Failed to fetch menu items");
        setFoods(data.filter(item => item.category === "food"));
        setDrinks(data.filter(item => item.category === "drink"));
      } catch (err) {
        console.error("Fetch menu error:", err);
      }
    };
    fetchMenuItems();
  }, [authTokens]);



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
            {foods.map((item) => (
              // --- THIS IS THE FIX ---
              // We explicitly map the prop name here.
              <MenuItem
                key={item.id}
                title={item.name}
                price={`Rs. ${item.price}`}
                tags={item.description || "No description"}
                imageUrl={item.image_url} // <-- Map snake_case to camelCase
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
            {drinks.map((item) => (
              // --- APPLY THE SAME FIX HERE ---
              <MenuItem
                key={item.id}
                title={item.name}
                price={`Rs. ${item.price}`}
                tags={item.description || "No description"}
                imageUrl={item.image_url} // <-- Map snake_case to camelCase
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
          <Cart 
            items={cartItems} 
            onRemove={removeFromCart}
            onAdd={addToCart}
            onRemoveCompletely={removeCompletelyFromCart}
            onCheckout={handleCheckout}
          />
        )}
      </div>
    </div>
  );
};

export default CanteenMenu;