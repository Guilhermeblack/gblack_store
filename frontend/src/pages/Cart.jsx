import React, { useEffect, useState } from 'react';
import api from '../api';
import { Trash2, Plus, Minus, ShoppingBag, Shield, Truck } from 'lucide-react';
import { Link } from 'react-router-dom';

const Cart = () => {
    const [cart, setCart] = useState(null);
    const [loading, setLoading] = useState(true);
    const [relatedProducts, setRelatedProducts] = useState([]);

    const fetchCart = async () => {
        try {
            const response = await api.get('cart/');
            setCart(response.data);

            if (response.data.items && response.data.items.length > 0) {
                const firstItem = response.data.items[0];
                fetchRelatedProducts(firstItem.produto.id);
            }
        } catch (error) {
            console.error('Error fetching cart:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchRelatedProducts = async (productId) => {
        try {
            const response = await api.get(`products/${productId}/related/`);
            setRelatedProducts(response.data);
        } catch (error) {
            console.error('Error fetching related products:', error);
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
            alert(error.response?.data?.error || 'Erro ao atualizar quantidade');
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

    const addToCart = async (productId) => {
        try {
            await api.post('cart/add_item/', {
                product_id: productId,
                quantity: 1
            });
            fetchCart();
        } catch (error) {
            console.error('Error adding to cart:', error);
            alert(error.response?.data?.error || 'Erro ao adicionar ao carrinho');
        }
    };

    if (loading) return (
        <div className="flex justify-center items-center h-screen bg-[#0a0a0a]">
            <div className="animate-pulse text-[#d4af37]">Carregando carrinho...</div>
        </div>
    );

    return (
        <div className="bg-[#0a0a0a] min-h-screen py-8">
            <div className="container mx-auto px-4">
                <h1 className="text-4xl font-bold mb-8 text-white">
                    Seu <span className="text-gradient">Carrinho</span>
                </h1>

                {!cart || cart.items.length === 0 ? (
                    <div className="text-center py-20 card-dark">
                        <ShoppingBag size={64} className="mx-auto text-gray-600 mb-4" />
                        <h2 className="text-2xl font-bold mb-2 text-white">Seu carrinho está vazio</h2>
                        <p className="text-gray-500 mb-6">Explore nossos produtos e encontre o que você procura.</p>
                        <Link to="/" className="btn-primary inline-block">
                            Começar a comprar
                        </Link>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <div className="lg:col-span-2 space-y-4">
                            <div className="bg-[#1a1a1a] border border-[#d4af37]/30 text-[#d4af37] p-4 rounded-lg text-sm flex items-center">
                                <span className="mr-2">⏱️</span>
                                Seus itens estão reservados por tempo limitado. Finalize sua compra para garantir o estoque.
                            </div>

                            {cart.items.map((item) => (
                                <div key={item.id} className="card-dark p-4 flex items-center space-x-4">
                                    <div className="w-24 h-24 bg-[#1a1a1a] rounded-lg overflow-hidden flex-shrink-0">
                                        {item.produto.img_prod_url ? (
                                            <img src={item.produto.img_prod_url} alt={item.produto.nome} className="w-full h-full object-cover" />
                                        ) : (
                                            <div className="w-full h-full flex items-center justify-center text-gray-500 text-xs">Sem Imagem</div>
                                        )}
                                    </div>

                                    <div className="flex-grow">
                                        <h3 className="font-semibold text-lg text-white">{item.produto.nome}</h3>
                                        <p className="text-gray-500">R$ {item.produto.preco}</p>
                                    </div>

                                    <div className="flex items-center space-x-3">
                                        <button
                                            onClick={() => updateQuantity(item.id, item.quantidade - 1)}
                                            className="p-2 bg-[#1a1a1a] hover:bg-[#333] rounded-lg text-white transition"
                                        >
                                            <Minus size={16} />
                                        </button>
                                        <span className="font-medium w-8 text-center text-white">{item.quantidade}</span>
                                        <button
                                            onClick={() => updateQuantity(item.id, item.quantidade + 1)}
                                            className="p-2 bg-[#1a1a1a] hover:bg-[#333] rounded-lg text-white transition"
                                        >
                                            <Plus size={16} />
                                        </button>
                                    </div>

                                    <div className="text-right min-w-[80px]">
                                        <p className="font-bold text-[#d4af37]">R$ {item.subtotal}</p>
                                    </div>

                                    <button
                                        onClick={() => removeItem(item.id)}
                                        className="text-red-500 hover:text-red-400 p-2 transition"
                                    >
                                        <Trash2 size={20} />
                                    </button>
                                </div>
                            ))}
                        </div>

                        <div className="card-dark p-6 h-fit sticky top-24">
                            <h3 className="text-xl font-bold mb-4 text-white">Resumo do Pedido</h3>
                            <div className="flex justify-between mb-2 text-gray-400">
                                <span>Subtotal</span>
                                <span className="text-white">R$ {cart.total}</span>
                            </div>
                            <div className="flex justify-between mb-4 text-gray-400">
                                <span>Frete</span>
                                <span className="text-green-500 font-semibold">Grátis</span>
                            </div>
                            <div className="border-t border-[#333] pt-4 flex justify-between font-bold text-xl mb-6">
                                <span className="text-white">Total</span>
                                <span className="text-gradient">R$ {cart.total}</span>
                            </div>
                            <Link to="/checkout" className="btn-primary w-full block text-center">
                                Finalizar Compra Agora
                            </Link>
                            <div className="flex items-center justify-center gap-4 mt-4 text-xs text-gray-500">
                                <span className="flex items-center gap-1"><Shield size={12} /> Seguro</span>
                                <span className="flex items-center gap-1"><Truck size={12} /> Frete Grátis</span>
                            </div>
                        </div>
                    </div>
                )}

                {/* Cross-selling Section */}
                {relatedProducts.length > 0 && (
                    <div className="mt-16">
                        <h2 className="text-2xl font-bold mb-6 text-white">Você também pode gostar</h2>
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                            {relatedProducts.map((product) => (
                                <div key={product.id} className="card-dark group">
                                    <div className="h-48 overflow-hidden">
                                        {product.img_prod_url ? (
                                            <img src={product.img_prod_url} alt={product.nome} className="w-full h-full object-cover group-hover:scale-110 transition duration-500" />
                                        ) : (
                                            <div className="w-full h-full flex items-center justify-center bg-[#1a1a1a] text-gray-500">Sem Imagem</div>
                                        )}
                                    </div>
                                    <div className="p-4">
                                        <h3 className="font-semibold mb-1 truncate text-white">{product.nome}</h3>
                                        <p className="text-[#d4af37] font-bold mb-3">R$ {product.preco}</p>
                                        <button
                                            onClick={() => addToCart(product.id)}
                                            className="btn-secondary w-full text-sm"
                                        >
                                            Adicionar ao Carrinho
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Cart;
