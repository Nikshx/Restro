// src/components/Navbar/Navbar.js

import React,  { useState, useContext } from 'react';
import { GiHamburgerMenu } from 'react-icons/gi';
import { MdOutlineRestaurantMenu } from 'react-icons/md';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import images from '../../constants/images';

import './Navbar.css';

const Navbar = () => {
  const [toggleMenu, setToggleMenu] = useState(false);
  const { user, logoutUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    navigate('/');
  };

  return (
    <nav className='app__navbar'>
      <div className="app__navbar-logo">
        <img src={images.gericht} alt="app logo" />
      </div>

      <ul className='app__navbar-links'>
        <li className='p__opensans'><Link to="/">Home</Link></li>
        <li className='p__opensans'><a href="/#menu">Menu</a></li>
        <li className='p__opensans'><Link to="/book-table">Book Table</Link></li>
        {user && (
          <li className='p__opensans'><Link to="/my-orders">My Orders</Link></li>
        )}
      </ul>

      <div className="app__navbar-login">
        {user ? (
          <>
            {/* The NotificationBell component has been removed from here */}
            <span className='p__opensans' style={{ color: 'white', marginRight: '1rem' }}>
              Hi, {user.username}
            </span>
            <div className="app__navbar-separator" />
            <a onClick={handleLogout} className='p__opensans' style={{ cursor: 'pointer' }}>Logout</a>
          </>
        ) : (
          <Link to="/auth" className='p__opensans'>Login / Register</Link>
        )}
      </div>

      <div className="app__navbar-smallscreen">
        {/* The NotificationBell component has been removed from here */}
        <GiHamburgerMenu color='#fff' fontSize={27} onClick={() => setToggleMenu(true)} />
       
        {toggleMenu && (
          <div className='app__navbar-smallscreen_overlay flex__center slide-bottom'>
            <MdOutlineRestaurantMenu fontSize={27} className='overlay__close' onClick={() => setToggleMenu(false)} />
            <ul className='app__navbar-smallscreen-links'>
              <li className='p__opensans'><Link to="/" onClick={() => setToggleMenu(false)}>Home</Link></li>
              <li className='p__opensans'><a href="/#menu" onClick={() => setToggleMenu(false)}>Menu</a></li>
              <li className='p__opensans'><Link to="/book-table" onClick={() => setToggleMenu(false)}>Book Table</Link></li>
              {user && (
                 <li className='p__opensans'><Link to="/my-orders" onClick={() => setToggleMenu(false)}>My Orders</Link></li>
              )}
              <li className='p__opensans'>
                {user ? (
                  <a onClick={() => { handleLogout(); setToggleMenu(false); }} style={{ cursor: 'pointer' }}>Logout</a>
                ) : (
                  <Link to="/auth" onClick={() => setToggleMenu(false)}>Login / Register</Link>
                )}
              </li>
            </ul>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;