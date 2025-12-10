import React, { useEffect, useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';
import { Shield, CreditCard, QrCode, Truck, MapPin, Check, Copy, CheckCircle } from 'lucide-react';

const Checkout = () => {
    const [step, setStep] = useState(1);
    const [cart, setCart] = useState(null);
    const [loading, setLoading] = useState(true);
    const [processing, setProcessing] = useState(false);
    const [copied, setCopied] = useState(false);

    // Form data
    const [address, setAddress] = useState({
        street: '',
        number: '',
        neighborhood: '',
        city: '',
        state: '',
        zip_code: ''
    });
    const [shippingOptions, setShippingOptions] = useState([]);
    const [selectedShipping, setSelectedShipping] = useState(null);
    const [paymentMethod, setPaymentMethod] = useState('PIX');
    const [shippingLoading, setShippingLoading] = useState(false);

    // Order result
    const [orderResult, setOrderResult] = useState(null);

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

    const handleAddressSubmit = async (e) => {
        e.preventDefault();
        setShippingLoading(true);

        try {
            // Calculate shipping
            const response = await api.post('orders/calculate_shipping/', {
                zip_code: address.zip_code
            });

            setShippingOptions(response.data.options);
            if (response.data.options.length > 0) {
                setSelectedShipping(response.data.options[0]);
            }
            setStep(2);
        } catch (error) {
            console.error('Error calculating shipping:', error);
            alert(error.response?.data?.error || 'Erro ao calcular frete');
        } finally {
            setShippingLoading(false);
        }
    };

    const handleShippingSubmit = () => {
        setStep(3);
    };

    const handlePaymentSubmit = async () => {
        setProcessing(true);
        try {
            // Save address
            const addressResponse = await api.post('address/', address);
            const addressId = addressResponse.data.id;

            // Process checkout
            const checkoutResponse = await api.post('orders/checkout/', {
                address_id: addressId,
                payment_method: paymentMethod,
                shipping_option: selectedShipping?.code
            });

            if (checkoutResponse.data.success) {
                setOrderResult(checkoutResponse.data);
                setStep(4);
            } else {
                alert('Erro no checkout: ' + (checkoutResponse.data.message || 'Erro desconhecido'));
            }
        } catch (error) {
            console.error('Error processing checkout:', error);
            const errorMessage = error.response?.data?.error || 'Erro ao processar pedido.';
            alert(errorMessage);
        } finally {
            setProcessing(false);
        }
    };

    const copyPixCode = () => {
        if (orderResult?.pix_data?.qr_code_text) {
            navigator.clipboard.writeText(orderResult.pix_data.qr_code_text);
            setCopied(true);
            setTimeout(() => setCopied(false), 3000);
        }
    };

    const getShippingPrice = () => {
        if (!selectedShipping) return 0;
        return parseFloat(selectedShipping.price);
    };

    const getTotal = () => {
        if (!cart) return 0;
        return parseFloat(cart.total) + getShippingPrice();
    };

    if (loading) return (
        <div className="flex justify-center items-center h-screen bg-[#0a0a0a]">
            <div className="animate-pulse text-[#d4af37]">Carregando...</div>
        </div>
    );

    if (!cart || cart.items.length === 0) return (
        <div className="flex justify-center items-center h-screen bg-[#0a0a0a] text-white">
            Carrinho vazio
        </div>
    );

    const inputClass = "w-full px-4 py-3 bg-[#1a1a1a] border border-[#333] text-white placeholder-gray-500 rounded-lg focus:outline-none focus:border-[#d4af37] transition";

    // Step indicator
    const StepIndicator = () => (
        <div className="flex justify-center mb-8">
            <div className="flex items-center gap-2">
                {[
                    { num: 1, icon: MapPin, label: 'Endereço' },
                    { num: 2, icon: Truck, label: 'Frete' },
                    { num: 3, icon: CreditCard, label: 'Pagamento' },
                    { num: 4, icon: Check, label: 'Confirmação' }
                ].map((s, i) => (
                    <React.Fragment key={s.num}>
                        <div className={`flex items-center gap-2 px-3 py-2 rounded-lg transition ${step >= s.num
                                ? 'bg-[#d4af37]/20 text-[#d4af37]'
                                : 'bg-[#1a1a1a] text-gray-500'
                            }`}>
                            <s.icon size={18} />
                            <span className="hidden sm:inline text-sm font-medium">{s.label}</span>
                        </div>
                        {i < 3 && <div className={`w-8 h-0.5 ${step > s.num ? 'bg-[#d4af37]' : 'bg-[#333]'}`} />}
                    </React.Fragment>
                ))}
            </div>
        </div>
    );

    // Order Summary Sidebar
    const OrderSummary = () => (
        <div className="card-dark p-6 h-fit sticky top-24">
            <h3 className="text-xl font-bold mb-4 text-white">Resumo do Pedido</h3>
            <div className="space-y-3 mb-4">
                {cart.items.map(item => (
                    <div key={item.id} className="flex justify-between text-sm">
                        <span className="text-gray-400">{item.quantidade}x {item.produto.nome}</span>
                        <span className="text-white">R$ {item.subtotal}</span>
                    </div>
                ))}
            </div>
            <div className="border-t border-[#333] pt-4 flex justify-between text-gray-400 mb-2">
                <span>Subtotal</span>
                <span className="text-white">R$ {cart.total}</span>
            </div>
            <div className="flex justify-between text-gray-400 mb-4">
                <span>Frete</span>
                {selectedShipping ? (
                    <span className={selectedShipping.is_free ? 'text-green-500 font-semibold' : 'text-white'}>
                        {selectedShipping.is_free ? 'Grátis' : `R$ ${selectedShipping.price}`}
                    </span>
                ) : (
                    <span className="text-gray-500">A calcular</span>
                )}
            </div>
            <div className="border-t border-[#333] pt-4 flex justify-between font-bold text-xl">
                <span className="text-white">Total</span>
                <span className="text-gradient">R$ {getTotal().toFixed(2)}</span>
            </div>
            <div className="flex items-center justify-center gap-2 mt-4 text-xs text-gray-500">
                <Shield size={14} />
                <span>Pagamento 100% seguro</span>
            </div>
        </div>
    );

    return (
        <div className="bg-[#0a0a0a] min-h-screen py-8">
            <div className="container mx-auto px-4">
                <h1 className="text-4xl font-bold mb-4 text-white text-center">
                    <span className="text-gradient">Checkout</span>
                </h1>

                <StepIndicator />

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-2">

                        {/* Step 1: Address */}
                        {step === 1 && (
                            <div className="card-dark p-6">
                                <h2 className="text-xl font-bold mb-4 text-white flex items-center gap-2">
                                    <MapPin className="text-[#d4af37]" /> Endereço de Entrega
                                </h2>
                                <form onSubmit={handleAddressSubmit} className="space-y-4">
                                    <div className="grid grid-cols-2 gap-4">
                                        <input
                                            name="zip_code"
                                            placeholder="CEP"
                                            required
                                            value={address.zip_code}
                                            className={`col-span-2 ${inputClass}`}
                                            onChange={handleAddressChange}
                                        />
                                        <input
                                            name="street"
                                            placeholder="Rua"
                                            required
                                            value={address.street}
                                            className={`col-span-2 ${inputClass}`}
                                            onChange={handleAddressChange}
                                        />
                                        <input
                                            name="number"
                                            placeholder="Número"
                                            required
                                            value={address.number}
                                            className={inputClass}
                                            onChange={handleAddressChange}
                                        />
                                        <input
                                            name="neighborhood"
                                            placeholder="Bairro"
                                            required
                                            value={address.neighborhood}
                                            className={inputClass}
                                            onChange={handleAddressChange}
                                        />
                                        <input
                                            name="city"
                                            placeholder="Cidade"
                                            required
                                            value={address.city}
                                            className={inputClass}
                                            onChange={handleAddressChange}
                                        />
                                        <input
                                            name="state"
                                            placeholder="Estado (UF)"
                                            required
                                            maxLength="2"
                                            value={address.state}
                                            className={inputClass}
                                            onChange={handleAddressChange}
                                        />
                                    </div>
                                    <button
                                        type="submit"
                                        disabled={shippingLoading}
                                        className="btn-primary w-full disabled:opacity-50"
                                    >
                                        {shippingLoading ? 'Calculando frete...' : 'Calcular Frete →'}
                                    </button>
                                </form>
                            </div>
                        )}

                        {/* Step 2: Shipping */}
                        {step === 2 && (
                            <div className="card-dark p-6">
                                <h2 className="text-xl font-bold mb-4 text-white flex items-center gap-2">
                                    <Truck className="text-[#d4af37]" /> Opções de Envio
                                </h2>
                                <div className="space-y-3 mb-6">
                                    {shippingOptions.map((option, i) => (
                                        <label
                                            key={i}
                                            className={`flex items-center justify-between border p-4 rounded-lg cursor-pointer transition ${selectedShipping?.code === option.code
                                                    ? 'border-[#d4af37] bg-[#d4af37]/10'
                                                    : 'border-[#333] hover:border-[#555]'
                                                }`}
                                        >
                                            <div className="flex items-center gap-3">
                                                <input
                                                    type="radio"
                                                    name="shipping"
                                                    checked={selectedShipping?.code === option.code}
                                                    onChange={() => setSelectedShipping(option)}
                                                    className="accent-[#d4af37]"
                                                />
                                                <div>
                                                    <p className="text-white font-medium">{option.name}</p>
                                                    <p className="text-gray-500 text-sm">
                                                        Entrega em até {option.delivery_days} dias úteis
                                                    </p>
                                                    {option.free_shipping_message && (
                                                        <p className="text-yellow-500 text-xs mt-1">
                                                            💡 {option.free_shipping_message}
                                                        </p>
                                                    )}
                                                </div>
                                            </div>
                                            <span className={`font-bold ${option.is_free ? 'text-green-500' : 'text-white'}`}>
                                                {option.is_free ? 'GRÁTIS' : `R$ ${option.price}`}
                                            </span>
                                        </label>
                                    ))}
                                </div>
                                <div className="flex gap-4">
                                    <button
                                        onClick={() => setStep(1)}
                                        className="btn-secondary flex-1"
                                    >
                                        ← Voltar
                                    </button>
                                    <button
                                        onClick={handleShippingSubmit}
                                        className="btn-primary flex-1"
                                    >
                                        Continuar →
                                    </button>
                                </div>
                            </div>
                        )}

                        {/* Step 3: Payment */}
                        {step === 3 && (
                            <div className="card-dark p-6">
                                <h2 className="text-xl font-bold mb-4 text-white flex items-center gap-2">
                                    <CreditCard className="text-[#d4af37]" /> Forma de Pagamento
                                </h2>
                                <div className="space-y-3 mb-6">
                                    <label className={`flex items-center space-x-3 border p-4 rounded-lg cursor-pointer transition ${paymentMethod === 'PIX' ? 'border-[#d4af37] bg-[#d4af37]/10' : 'border-[#333] hover:border-[#555]'
                                        }`}>
                                        <input
                                            type="radio"
                                            name="payment"
                                            value="PIX"
                                            checked={paymentMethod === 'PIX'}
                                            onChange={(e) => setPaymentMethod(e.target.value)}
                                            className="accent-[#d4af37]"
                                        />
                                        <QrCode size={20} className="text-[#d4af37]" />
                                        <div className="flex-1">
                                            <span className="text-white font-medium">PIX</span>
                                            <p className="text-gray-500 text-sm">Aprovação imediata</p>
                                        </div>
                                        <span className="text-green-500 text-xs">Recomendado</span>
                                    </label>
                                    <label className={`flex items-center space-x-3 border p-4 rounded-lg cursor-pointer transition ${paymentMethod === 'CARD' ? 'border-[#d4af37] bg-[#d4af37]/10' : 'border-[#333] hover:border-[#555]'
                                        }`}>
                                        <input
                                            type="radio"
                                            name="payment"
                                            value="CARD"
                                            checked={paymentMethod === 'CARD'}
                                            onChange={(e) => setPaymentMethod(e.target.value)}
                                            className="accent-[#d4af37]"
                                        />
                                        <CreditCard size={20} className="text-[#d4af37]" />
                                        <div className="flex-1">
                                            <span className="text-white font-medium">Cartão de Crédito</span>
                                            <p className="text-gray-500 text-sm">Em até 3x sem juros</p>
                                        </div>
                                    </label>
                                </div>
                                <div className="flex gap-4">
                                    <button
                                        onClick={() => setStep(2)}
                                        className="btn-secondary flex-1"
                                    >
                                        ← Voltar
                                    </button>
                                    <button
                                        onClick={handlePaymentSubmit}
                                        disabled={processing}
                                        className="btn-primary flex-1 disabled:opacity-50"
                                    >
                                        {processing ? 'Processando...' : 'Confirmar Pedido →'}
                                    </button>
                                </div>
                            </div>
                        )}

                        {/* Step 4: Confirmation */}
                        {step === 4 && orderResult && (
                            <div className="card-dark p-6 text-center">
                                <CheckCircle size={64} className="mx-auto text-green-500 mb-4" />
                                <h2 className="text-2xl font-bold text-white mb-2">
                                    Pedido Realizado!
                                </h2>
                                <p className="text-gray-400 mb-6">
                                    Pedido #{orderResult.venda_id} criado com sucesso
                                </p>

                                {orderResult.pix_data && (
                                    <div className="bg-[#1a1a1a] rounded-lg p-6 mb-6">
                                        <h3 className="text-lg font-bold text-white mb-4">
                                            Pague com PIX
                                        </h3>

                                        {/* QR Code placeholder - in production, use a QR code library */}
                                        <div className="bg-white p-4 rounded-lg inline-block mb-4">
                                            <div className="w-48 h-48 bg-gray-100 flex items-center justify-center">
                                                <QrCode size={120} className="text-gray-800" />
                                            </div>
                                        </div>

                                        <p className="text-gray-400 text-sm mb-4">
                                            Ou copie o código PIX:
                                        </p>

                                        <div className="flex gap-2 max-w-md mx-auto">
                                            <input
                                                type="text"
                                                readOnly
                                                value={orderResult.pix_data.qr_code_text}
                                                className="flex-1 px-4 py-2 bg-[#0a0a0a] border border-[#333] rounded-lg text-gray-400 text-sm truncate"
                                            />
                                            <button
                                                onClick={copyPixCode}
                                                className={`px-4 py-2 rounded-lg font-medium transition ${copied
                                                        ? 'bg-green-500 text-white'
                                                        : 'bg-[#d4af37] text-black hover:bg-[#c4a030]'
                                                    }`}
                                            >
                                                {copied ? <Check size={20} /> : <Copy size={20} />}
                                            </button>
                                        </div>

                                        {copied && (
                                            <p className="text-green-500 text-sm mt-2">
                                                ✓ Código copiado!
                                            </p>
                                        )}

                                        <p className="text-yellow-500 text-sm mt-4">
                                            ⏱️ Este código expira em 30 minutos
                                        </p>
                                    </div>
                                )}

                                <button
                                    onClick={() => navigate('/')}
                                    className="btn-primary"
                                >
                                    Voltar para a Loja
                                </button>
                            </div>
                        )}
                    </div>

                    {/* Sidebar */}
                    <div className={step === 4 ? 'hidden lg:block' : ''}>
                        <OrderSummary />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Checkout;
