import React, { useEffect, useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';

const Checkout = () => {
    const [cart, setCart] = useState(null);
    const [loading, setLoading] = useState(true);
    const [address, setAddress] = useState({
        street: '',
        number: '',
        neighborhood: '',
        city: '',
        state: '',
        zip_code: ''
    });
    const [paymentMethod, setPaymentMethod] = useState('PIX');
    const navigate = useNavigate();

    useEffect(() => {
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
        fetchCart();
    }, []);

    const handleAddressChange = (e) => {
        setAddress({ ...address, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // 1. Save address
            const addressResponse = await api.post('address/', address);
            const addressId = addressResponse.data.id;

            // 2. Process checkout
            const checkoutResponse = await api.post('orders/checkout/', {
                address_id: addressId,
                payment_method: paymentMethod
            });

            if (checkoutResponse.data.success) {
                alert('Pedido realizado com sucesso!');
                navigate('/'); // Or navigate to a success page / orders page
            } else {
                alert('Erro no checkout: ' + (checkoutResponse.data.message || 'Erro desconhecido'));
            }

        } catch (error) {
            console.error('Error processing checkout:', error);
            const errorMessage = error.response?.data?.error || 'Erro ao processar pedido.';
            alert(errorMessage);
        }
    };

    if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;
    if (!cart || cart.items.length === 0) return <div className="text-center py-20">Carrinho vazio</div>;

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold mb-8">Checkout</h1>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                <div>
                    <h2 className="text-xl font-bold mb-4">Endereço de Entrega</h2>
                    <form id="checkout-form" onSubmit={handleSubmit} className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <input
                                name="street"
                                placeholder="Rua"
                                required
                                className="col-span-2 border p-3 rounded-lg w-full"
                                onChange={handleAddressChange}
                            />
                            <input
                                name="number"
                                placeholder="Número"
                                required
                                className="border p-3 rounded-lg w-full"
                                onChange={handleAddressChange}
                            />
                            <input
                                name="neighborhood"
                                placeholder="Bairro"
                                required
                                className="border p-3 rounded-lg w-full"
                                onChange={handleAddressChange}
                            />
                            <input
                                name="city"
                                placeholder="Cidade"
                                required
                                className="border p-3 rounded-lg w-full"
                                onChange={handleAddressChange}
                            />
                            <input
                                name="state"
                                placeholder="Estado (UF)"
                                required
                                maxLength="2"
                                className="border p-3 rounded-lg w-full"
                                onChange={handleAddressChange}
                            />
                            <input
                                name="zip_code"
                                placeholder="CEP"
                                required
                                className="col-span-2 border p-3 rounded-lg w-full"
                                onChange={handleAddressChange}
                            />
                        </div>

                        <h2 className="text-xl font-bold mt-8 mb-4">Pagamento</h2>
                        <div className="space-y-2">
                            <label className="flex items-center space-x-2 border p-4 rounded-lg cursor-pointer hover:bg-gray-50">
                                <input
                                    type="radio"
                                    name="payment"
                                    value="PIX"
                                    checked={paymentMethod === 'PIX'}
                                    onChange={(e) => setPaymentMethod(e.target.value)}
                                />
                                <span>PIX</span>
                            </label>
                            <label className="flex items-center space-x-2 border p-4 rounded-lg cursor-pointer hover:bg-gray-50">
                                <input
                                    type="radio"
                                    name="payment"
                                    value="CARD"
                                    checked={paymentMethod === 'CARD'}
                                    onChange={(e) => setPaymentMethod(e.target.value)}
                                />
                                <span>Cartão de Crédito</span>
                            </label>
                        </div>
                    </form>
                </div>

                <div className="bg-gray-50 p-6 rounded-xl h-fit">
                    <h3 className="text-xl font-bold mb-4">Resumo do Pedido</h3>
                    <div className="space-y-2 mb-4">
                        {cart.items.map(item => (
                            <div key={item.id} className="flex justify-between text-sm">
                                <span>{item.quantidade}x {item.produto.nome}</span>
                                <span>R$ {item.subtotal}</span>
                            </div>
                        ))}
                    </div>
                    <div className="border-t pt-4 flex justify-between font-bold text-lg mb-6">
                        <span>Total</span>
                        <span>R$ {cart.total}</span>
                    </div>
                    <button
                        type="submit"
                        form="checkout-form"
                        className="w-full bg-black text-white py-3 rounded-lg font-semibold hover:bg-gray-800 transition"
                    >
                        Confirmar Pedido
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Checkout;
