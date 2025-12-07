import React from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { LayoutDashboard, Package, ShoppingBag, LogOut } from 'lucide-react';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

const AdminLayout = () => {
    const { logout } = useContext(AuthContext);
    const location = useLocation();

    const isActive = (path) => location.pathname === path;

    return (
        <div className="flex h-screen bg-gray-100">
            {/* Sidebar */}
            <aside className="w-64 bg-gray-900 text-white flex flex-col">
                <div className="p-6 border-b border-gray-800">
                    <h1 className="text-2xl font-bold tracking-wider">GBLACK ADMIN</h1>
                </div>

                <nav className="flex-grow p-4 space-y-2">
                    <Link
                        to="/admin"
                        className={`flex items-center space-x-3 p-3 rounded-lg transition ${isActive('/admin') ? 'bg-gray-800 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'}`}
                    >
                        <LayoutDashboard size={20} />
                        <span>Dashboard</span>
                    </Link>

                    <Link
                        to="/admin/products"
                        className={`flex items-center space-x-3 p-3 rounded-lg transition ${isActive('/admin/products') ? 'bg-gray-800 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'}`}
                    >
                        <Package size={20} />
                        <span>Produtos</span>
                    </Link>

                    <Link
                        to="/admin/orders"
                        className={`flex items-center space-x-3 p-3 rounded-lg transition ${isActive('/admin/orders') ? 'bg-gray-800 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'}`}
                    >
                        <ShoppingBag size={20} />
                        <span>Pedidos</span>
                    </Link>

                    <Link
                        to="/admin/feed"
                        className={`flex items-center space-x-3 p-3 rounded-lg transition ${isActive('/admin/feed') ? 'bg-gray-800 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'}`}
                    >
                        <LayoutDashboard size={20} />
                        <span>Feed</span>
                    </Link>
                </nav>

                <div className="p-4 border-t border-gray-800">
                    <button
                        onClick={logout}
                        className="flex items-center space-x-3 p-3 w-full rounded-lg text-gray-400 hover:bg-red-600 hover:text-white transition"
                    >
                        <LogOut size={20} />
                        <span>Sair</span>
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-grow overflow-y-auto p-8">
                <Outlet />
            </main>
        </div>
    );
};

export default AdminLayout;
