import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { CanteenHeader, CanteenMenu } from './container';
import AuthPage from './pages/AuthPage';
import MainLayout from './Layouts/MainLayout'; 
import './App.css';
import BookTable from './components/BookTable/BookTable';
import OrderConfirmationPage from './pages/OrderConfirmationPage';
import OrderHistoryPage from './pages/OrderHistoryPage';
function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>

         
          <Route path="/auth" element={<AuthPage />} />


        
          <Route element={<MainLayout />}>
            <Route path="/" element={
              <>
                <CanteenHeader />
                <CanteenMenu />
              </>
            } />
            <Route path="/book-table" element={<BookTable />} />
            <Route path="/order/:orderId" element={<OrderConfirmationPage />} />
            <Route path="/my-orders" element={<OrderHistoryPage />} />

          </Route>
          
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;