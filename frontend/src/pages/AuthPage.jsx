import React, { useState } from 'react';
import Login from '../components/Auth/Login'; // Create this
import Register from '../components/Auth/Register'; // Create this
import './AuthPage.css';
const AuthPage = () => {
    const [showLogin, setShowLogin] = useState(true);

    return (
        <div className="auth__page"> 
            <div className="auth__container"> 
                {showLogin ? <Login /> : <Register />}
                <button className="auth__toggle-btn" onClick={() => setShowLogin(!showLogin)}>
                    {showLogin ? "Need an account? Register" : "Already have an account? Login"}
                </button>
            </div>
        </div>
    );
};

export default AuthPage;