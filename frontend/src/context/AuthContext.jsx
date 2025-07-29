import React, { createContext, useState, useEffect } from 'react';
import {jwtDecode} from 'jwt-decode';  // fixed import

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    // parse tokens from localStorage, or null if not found
    const [authTokens, setAuthTokens] = useState(() => {
        const tokens = localStorage.getItem('authTokens');
        return tokens ? JSON.parse(tokens) : null;
    });

    // decode user from access token if available
    const [user, setUser] = useState(() => {
        const tokens = localStorage.getItem('authTokens');
        if (tokens) {
            const parsedTokens = JSON.parse(tokens);
            return parsedTokens.access ? jwtDecode(parsedTokens.access) : null;
        }
        return null;
    });

    const loginUser = (tokens) => {
        setAuthTokens(tokens);
        setUser(tokens.access ? jwtDecode(tokens.access) : null);
        localStorage.setItem('authTokens', JSON.stringify(tokens));
    };

    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
    };

    const contextData = {
        user,
        authTokens,
        loginUser,
        logoutUser,
    };

    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    );
};
