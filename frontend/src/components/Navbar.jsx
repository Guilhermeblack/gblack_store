import React, { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ShoppingCart, User, Menu, LogOut } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import api from '../api';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const [cartCount, setCartCount] = useState(0);

  const fetchCartCount = async () => {
    try {
      const response = await api.get('cart/');
      const items = response.data?.items || [];
      const totalItems = items.reduce((sum, item) => sum + item.quantidade, 0);
      setCartCount(totalItems);
    } catch (error) {
      // Cart might not exist yet, ignore error
      setCartCount(0);
    }
  };

  useEffect(() => {
    fetchCartCount();

    // Listen for cart updates
    const handleCartUpdate = () => fetchCartCount();
    window.addEventListener('cartUpdated', handleCartUpdate);

    return () => window.removeEventListener('cartUpdated', handleCartUpdate);
  }, [user]);

  return (
    <nav className="bg-primary text-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold tracking-wider">
          GBLACK
        </Link>

        <div className="hidden md:flex space-x-6">
          <Link to="/" className="hover:text-gray-300 transition">Home</Link>
          <Link to="/feed" className="hover:text-gray-300 transition">Feed</Link>
          <Link to="/products" className="hover:text-gray-300 transition">Produtos</Link>
        </div>

        <div className="flex items-center space-x-4">
          <Link to="/cart" className="relative hover:text-gray-300 transition">
            <ShoppingCart size={24} />
            {cartCount > 0 && (
              <span className="absolute -top-2 -right-2 bg-red-500 text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold">
                {cartCount > 99 ? '99+' : cartCount}
              </span>
            )}
          </Link>

          {user ? (
            <>
              <span className="hidden md:inline text-sm">Olá, {user.username}</span>
              <button onClick={logout} className="hover:text-gray-300 transition" title="Sair">
                <LogOut size={24} />
              </button>
            </>
          ) : (
            <Link to="/login" className="hover:text-gray-300 transition">
              <User size={24} />
            </Link>
          )}

          <button className="md:hidden">
            <Menu size={24} />
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
