import React, { useState, useContext } from 'react'; 
import { useNavigate } from 'react-router-dom';     
import { AuthContext } from '../../context/AuthContext'; 

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(''); 
    const { loginUser } = useContext(AuthContext); 
    const navigate = useNavigate();               

    // Helper function to automatically log in after registration
    const performLogin = async () => {
        const response = await fetch('/api/token/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
            credentials: 'include', 
        });
        const data = await response.json();
        if (response.ok) {
            loginUser(data);
            navigate('/');
        } else {
            throw new Error('Registration succeeded, but auto-login failed. Please log in manually.');
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');    

        try {
            const response = await fetch('http://localhost:8000/api/register/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();

            if (!response.ok) {
                const errorMessage = data.username ? `Username: ${data.username[0]}` : 'Registration failed.';
                throw new Error(errorMessage);
            }

            // Instead of showing a success message, just log them in.
            await performLogin();

        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <form onSubmit={handleSubmit} style={{ width: '100%' }}>
            <h2>Create Account</h2>
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
            <button type="submit" className="custom__button">Register</button>
        </form>
    );
};

export default Register;