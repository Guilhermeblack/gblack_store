import React, { useEffect, useState } from 'react';
import api from '../api';
import { Trash2, Plus, Minus, ShoppingBag } from 'lucide-react';
import { Link } from 'react-router-dom';

const Cart = () => {
    const [cart, setCart] = useState(null);
    const [loading, setLoading] = useState(true);
    const [relatedProducts, setRelatedProducts] = useState([]);

    const fetchCart = async () => {
        try {
            const response = await api.get('cart/');
            setCart(response.data);

            // If cart has items, fetch related products based on the first item
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
            fetchCart(); // Refresh cart
            alert('Produto adicionado ao carrinho!');
        } catch (error) {
            console.error('Error adding to cart:', error);
            alert(error.response?.data?.error || 'Erro ao adicionar ao carrinho');
        }
    };

    if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold mb-2">Seu Carrinho</h1>

            {!cart || cart.items.length === 0 ? (
                <div className="text-center py-20 bg-white rounded-xl shadow-sm">
                    <ShoppingBag size={64} className="mx-auto text-gray-300 mb-4" />
                    <h2 className="text-2xl font-bold mb-2">Seu carrinho está vazio</h2>
                    <p className="text-gray-500 mb-6">Explore nossos produtos e encontre o que você procura.</p>
                    <Link to="/" className="inline-block bg-black text-white px-8 py-3 rounded-lg font-semibold hover:bg-gray-800 transition">
                        Começar a comprar
                    </Link>
                </div>
            ) : (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-2 space-y-4">
                        <div className="bg-blue-50 text-blue-800 p-4 rounded-lg text-sm flex items-center">
                            <span className="mr-2">ℹ️</span>
                            Seus itens estão reservados por tempo limitado. Finalize sua compra para garantir o estoque.
                        </div>

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
                            <span className="text-green-600">Grátis</span>
                        </div>
                        <div className="border-t pt-4 flex justify-between font-bold text-lg mb-6">
                            <span>Total</span>
                            <span>R$ {cart.total}</span>
                        </div>
                        <Link to="/checkout" className="w-full bg-black text-white py-3 rounded-lg font-semibold hover:bg-gray-800 transition block text-center">
                            Finalizar Compra Agora
                        </Link>
                        <p className="text-xs text-center text-gray-500 mt-4">
                            Compra 100% segura e garantida.
                        </p>
                    </div>
                </div>
            )}

            {/* Cross-selling Section */}
            {relatedProducts.length > 0 && (
                <div className="mt-16">
                    <h2 className="text-2xl font-bold mb-6">Você também pode gostar</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                        {relatedProducts.map((product) => (
                            <div key={product.id} className="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition">
                                <div className="h-48 bg-gray-100">
                                    {product.img_prod_url ? (
                                        <img src={product.img_prod_url} alt={product.nome} className="w-full h-full object-cover" />
                                    ) : (
                                        <div className="w-full h-full flex items-center justify-center text-gray-400">Sem Imagem</div>
                                    )}
                                </div>
                                <div className="p-4">
                                    <h3 className="font-semibold mb-1 truncate">{product.nome}</h3>
                                    <p className="text-gray-900 font-bold mb-3">R$ {product.preco}</p>
                                    <button
                                        onClick={() => addToCart(product.id)}
                                        className="w-full bg-gray-900 text-white py-2 rounded-lg text-sm font-medium hover:bg-gray-800 transition"
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
    );
};

export default Cart;
