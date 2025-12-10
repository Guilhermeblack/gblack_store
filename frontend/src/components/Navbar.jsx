import React, { useContext, useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ShoppingCart, User, Menu, LogOut, X } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import api from '../api';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const [cartCount, setCartCount] = useState(0);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const fetchCartCount = async () => {
    try {
      const response = await api.get('cart/');
      const items = response.data?.items || [];
      const totalItems = items.reduce((sum, item) => sum + item.quantidade, 0);
      setCartCount(totalItems);
    } catch (error) {
      setCartCount(0);
    }
  };

  useEffect(() => {
    fetchCartCount();
    const handleCartUpdate = () => fetchCartCount();
    window.addEventListener('cartUpdated', handleCartUpdate);
    return () => window.removeEventListener('cartUpdated', handleCartUpdate);
  }, [user]);

  const isActive = (path) => location.pathname === path;

  const navLinks = [
    { path: '/', label: 'Home' },
    { path: '/products', label: 'Produtos' },
    { path: '/feed', label: 'Feed' },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-black tracking-wider text-gradient">
          GBLACK
        </Link>

        {/* Desktop Menu */}
        <div className="hidden md:flex space-x-8">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={`font-medium transition-all duration-300 hover:text-[#d4af37] ${isActive(link.path) ? 'text-[#d4af37]' : 'text-white'
                }`}
            >
              {link.label}
            </Link>
          ))}
        </div>

        <div className="flex items-center space-x-4">
          <Link to="/cart" className="relative hover:text-[#d4af37] transition group">
            <ShoppingCart size={24} />
            {cartCount > 0 && (
              <span className="absolute -top-2 -right-2 bg-[#d4af37] text-black text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold animate-pulse">
                {cartCount > 99 ? '99+' : cartCount}
              </span>
            )}
          </Link>

          {user ? (
            <>
              <span className="hidden md:inline text-sm text-gray-300">
                Olá, <strong className="text-white">{user.username}</strong>
              </span>
              {user.is_staff && (
                <Link to="/admin" className="text-[#d4af37] text-sm font-semibold hover:underline">
                  Admin
                </Link>
              )}
              <button onClick={logout} className="hover:text-[#d4af37] transition" title="Sair">
                <LogOut size={22} />
              </button>
            </>
          ) : (
            <Link to="/login" className="btn-primary py-2 px-4 text-sm hidden md:inline-block">
              Entrar
            </Link>
          )}

          {/* Mobile Menu Button */}
          <button className="md:hidden" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-[#1a1a1a] border-t border-[#333] animate-fadeIn">
          <div className="container mx-auto px-4 py-4 flex flex-col space-y-4">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`font-medium py-2 ${isActive(link.path) ? 'text-[#d4af37]' : 'text-white'
                  }`}
              >
                {link.label}
              </Link>
            ))}
            {!user && (
              <Link
                to="/login"
                onClick={() => setMobileMenuOpen(false)}
                className="btn-primary text-center"
              >
                Entrar
              </Link>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
