// src/layouts/MainLayout.js

import React from 'react'; // Removed useEffect, useContext, useRef
import { Outlet } from 'react-router-dom';
import { Navbar } from '../components';
// Removed AuthContext as it's not directly used here anymore for the socket
import { ToastContainer } from 'react-toastify'; // Keep for other notifications

// No longer need the NotificationProvider or the complex MainLayoutContent structure

const MainLayout = () => {
  // --- THE ENTIRE useEffect HOOK FOR WEBSOCKETS HAS BEEN DELETED ---

  return (
    <div>
      {/* You can keep ToastContainer for non-real-time notifications */}
      {/* like "Order placed successfully!" */}
      <ToastContainer
        position="top-right"
        autoClose={5000}
        theme="dark"
      />
      
      <Navbar />
      <main>
        <Outlet />
      </main>
      {/* <Footer /> */}
    </div>
  );
};

export default MainLayout;