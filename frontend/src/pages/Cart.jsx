import React, { useEffect, useState } from 'react';
import api from '../api';
import { Trash2, Plus, Minus } from 'lucide-react';
import { Link } from 'react-router-dom';

const Cart = () => {
    const [cart, setCart] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchCart = async () => {
        try {
            const response = await api.get('cart/');
            setCart(response.data);
        } catch (error) {
            console.error('Error fetching cart:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCart();
    }, []);

    const updateQuantity = async (itemId, newQuantity) => {
        try {
            await api.post('cart/update_quantity/', {
                item_id: itemId,
                quantity: newQuantity
            });
            fetchCart();
        } catch (error) {
            console.error('Error updating quantity:', error);
        }
    };

    const removeItem = async (itemId) => {
        try {
            await api.post('cart/remove_item/', {
                item_id: itemId
            });
            fetchCart();
        } catch (error) {
            console.error('Error removing item:', error);
        }
    };

    if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;

    if (!cart || cart.items.length === 0) {
        return (
            <div className="container mx-auto px-4 py-20 text-center">
                <h2 className="text-2xl font-bold mb-4">Seu carrinho está vazio</h2>
                <Link to="/" className="text-blue-600 hover:underline">Continuar comprando</Link>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold mb-8">Seu Carrinho</h1>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 space-y-4">
                    {cart.items.map((item) => (
                        <div key={item.id} className="bg-white p-4 rounded-xl shadow-sm flex items-center space-x-4">
                            <div className="w-24 h-24 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
                                {item.produto.img_prod_url ? (
                                    <img src={item.produto.img_prod_url} alt={item.produto.nome} className="w-full h-full object-cover" />
                                ) : (
                                    <div className="w-full h-full flex items-center justify-center text-gray-400 text-xs">Sem Imagem</div>
                                )}
                            </div>

                            <div className="flex-grow">
                                <h3 className="font-semibold text-lg">{item.produto.nome}</h3>
                                <p className="text-gray-500">R$ {item.produto.preco}</p>
                            </div>

                            <div className="flex items-center space-x-3">
                                <button
                                    onClick={() => updateQuantity(item.id, item.quantidade - 1)}
                                    className="p-1 hover:bg-gray-100 rounded"
                                >
                                    <Minus size={16} />
                                </button>
                                <span className="font-medium w-8 text-center">{item.quantidade}</span>
                                <button
                                    onClick={() => updateQuantity(item.id, item.quantidade + 1)}
                                    className="p-1 hover:bg-gray-100 rounded"
                                >
                                    <Plus size={16} />
                                </button>
                            </div>

                            <div className="text-right min-w-[80px]">
                                <p className="font-bold">R$ {item.subtotal}</p>
                            </div>

                            <button
                                onClick={() => removeItem(item.id)}
                                className="text-red-500 hover:text-red-700 p-2"
                            >
                                <Trash2 size={20} />
                            </button>
                        </div>
                    ))}
                </div>

                <div className="bg-white p-6 rounded-xl shadow-sm h-fit">
                    <h3 className="text-xl font-bold mb-4">Resumo do Pedido</h3>
                    <div className="flex justify-between mb-2">
                        <span>Subtotal</span>
                        <span>R$ {cart.total}</span>
                    </div>
                    <div className="flex justify-between mb-4">
                        <span>Frete</span>
                        <span>Grátis</span>
                    </div>
                    <div className="border-t pt-4 flex justify-between font-bold text-lg mb-6">
                        <span>Total</span>
                        <span>R$ {cart.total}</span>
                    </div>
                    <Link to="/checkout" className="w-full bg-black text-white py-3 rounded-lg font-semibold hover:bg-gray-800 transition block text-center">
                        Finalizar Compra
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default Cart;
