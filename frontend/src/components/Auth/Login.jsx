// src/components/Auth/Login.js

import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { loginUser } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await fetch('/api/token/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),

                // tells the browser to send cookies with this cross-origin request.
                credentials: 'include', 
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Invalid username or password.');
            }

            loginUser(data);
            navigate('/');
            
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <form onSubmit={handleSubmit} style={{ width: '100%' }}>
            <h2>Login</h2>
            <input 
                type="text" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)} 
                placeholder="Username" 
                required 
            />
            <input 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
                placeholder="Password" 
                required 
            />
            {error && <p className="auth__error">{error}</p>}
            <button type="submit" className="custom__button">Login</button>
        </form>
    );
};
 
export default Login;