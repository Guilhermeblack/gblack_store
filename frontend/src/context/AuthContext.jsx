import React, { createContext, useState, useEffect } from 'react';
import api from '../api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkUser = async () => {
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    const response = await api.get('user/me/');
                    setUser(response.data);
                } catch (error) {
                    console.error('Invalid token', error);
                    localStorage.removeItem('token');
                }
            }
            setLoading(false);
        };
        checkUser();
    }, []);

    const login = async (username, password) => {
        const response = await api.post('api-token-auth/', { username, password });
        const { token } = response.data;
        localStorage.setItem('token', token);

        // Fetch user details
        const userResponse = await api.get('user/me/');
        setUser(userResponse.data);
        return true;
    };

    const register = async (userData) => {
        await api.post('user/', userData);
        return await login(userData.username, userData.password);
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, register, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};
