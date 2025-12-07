import React, { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const AdminRoute = () => {
    const { user, loading } = useContext(AuthContext);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!user || !user.is_staff) {
        return <Navigate to="/" replace />;
    }

    return <Outlet />;
};

export default AdminRoute;
