import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';
import { ShoppingCart, ArrowLeft, X, ChevronLeft, ChevronRight, Check, AlertCircle } from 'lucide-react';

const ProductDetail = () => {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [relatedProducts, setRelatedProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [quantity, setQuantity] = useState(1);
    const [showCarousel, setShowCarousel] = useState(false);
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const [toast, setToast] = useState(null); // { type: 'success' | 'error', message: string }

    // For demo purposes, we'll simulate multiple images
    const getProductImages = () => {
        if (!product) return [];
        // If product has multiple images, use them. Otherwise, use the main image.
        return product.img_prod_url ? [product.img_prod_url] : [];
    };

    const fetchProduct = async () => {
        try {
            const response = await api.get(`products/${id}/`);
            setProduct(response.data);

            // Fetch related products
            try {
                const relatedResponse = await api.get(`products/${id}/related/`);
                setRelatedProducts(relatedResponse.data);
            } catch (e) {
                console.error('Error fetching related products:', e);
            }
        } catch (error) {
            console.error('Error fetching product:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchProduct();
    }, [id]);

    const showToast = (type, message) => {
        setToast({ type, message });
        setTimeout(() => setToast(null), 3000);
    };

    const addToCart = async () => {
        try {
            await api.post('cart/add_item/', {
                product_id: product.id,
                quantity: quantity
            });
            showToast('success', 'Produto adicionado ao carrinho!');
            window.dispatchEvent(new Event('cartUpdated'));
            // Refresh product data to update stock
            fetchProduct();
            setQuantity(1);
        } catch (error) {
            console.error('Error adding to cart:', error);
            showToast('error', error.response?.data?.error || 'Erro ao adicionar ao carrinho.');
        }
    };

    const images = getProductImages();

    if (loading) return <div className="flex justify-center items-center h-screen bg-[#0a0a0a]"><div className="animate-pulse text-[#d4af37]">Carregando...</div></div>;
    if (!product) return <div className="text-center py-20 bg-[#0a0a0a] text-white">Produto não encontrado</div>;

    return (
        <>
            {/* Toast Notification */}
            {toast && (
                <div className={`fixed top-20 left-1/2 transform -translate-x-1/2 z-50 px-6 py-3 rounded-lg shadow-lg flex items-center gap-2 animate-pulse ${toast.type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
                    }`}>
                    {toast.type === 'success' ? <Check size={20} /> : <AlertCircle size={20} />}
                    {toast.message}
                </div>
            )}

            {/* Carousel Modal */}
            {showCarousel && images.length > 0 && (
                <div className="fixed inset-0 bg-black/90 z-50 flex items-center justify-center">
                    <button
                        onClick={() => setShowCarousel(false)}
                        className="absolute top-4 right-4 text-white hover:text-gray-300"
                    >
                        <X size={32} />
                    </button>

                    <button
                        onClick={() => setCurrentImageIndex((currentImageIndex - 1 + images.length) % images.length)}
                        className="absolute left-4 text-white hover:text-gray-300"
                    >
                        <ChevronLeft size={48} />
                    </button>

                    <div className="max-w-4xl max-h-[80vh] flex flex-col items-center">
                        <img
                            src={images[currentImageIndex]}
                            alt={product.nome}
                            className="max-w-full max-h-[60vh] object-contain"
                        />
                        <div className="mt-6 text-center text-white px-8">
                            <h2 className="text-2xl font-bold mb-2">{product.nome}</h2>
                            <p className="text-gray-300 mb-4">{product.descricao}</p>
                            <p className="text-3xl font-bold text-green-400">R$ {product.preco}</p>
                        </div>
                        <button
                            onClick={addToCart}
                            className="mt-4 bg-white text-black py-3 px-8 rounded-lg font-semibold hover:bg-gray-200 transition flex items-center"
                        >
                            <ShoppingCart size={20} className="mr-2" />
                            Comprar Agora
                        </button>
                    </div>

                    <button
                        onClick={() => setCurrentImageIndex((currentImageIndex + 1) % images.length)}
                        className="absolute right-4 text-white hover:text-gray-300"
                    >
                        <ChevronRight size={48} />
                    </button>

                    {/* Dots */}
                    <div className="absolute bottom-8 flex gap-2">
                        {images.map((_, idx) => (
                            <button
                                key={idx}
                                onClick={() => setCurrentImageIndex(idx)}
                                className={`w-3 h-3 rounded-full ${idx === currentImageIndex ? 'bg-white' : 'bg-gray-500'}`}
                            />
                        ))}
                    </div>
                </div>
            )}

            <div className="bg-[#0a0a0a] min-h-screen pb-28">
                <div className="container mx-auto px-4 py-8">
                    <Link to="/products" className="inline-flex items-center text-gray-400 hover:text-[#d4af37] mb-8 transition">
                        <ArrowLeft size={20} className="mr-2" /> Voltar para Produtos
                    </Link>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                        <div
                            className="card-dark cursor-pointer hover:scale-[1.02] transition-transform"
                            onClick={() => images.length > 0 && setShowCarousel(true)}
                        >
                            {product.img_prod_url ? (
                                <img src={product.img_prod_url} alt={product.nome} className="w-full aspect-square object-cover" />
                            ) : (
                                <div className="w-full aspect-square flex items-center justify-center bg-[#1a1a1a] text-gray-500">Sem Imagem</div>
                            )}
                        </div>

                        <div>
                            <span className="text-[#d4af37] text-sm font-semibold uppercase tracking-wider">
                                {product.tipo === 'R' ? 'Relógio' : product.tipo === 'A' ? 'Acessório' : 'Vestuário'}
                            </span>
                            <h1 className="text-4xl font-black text-white mb-4 mt-2">{product.nome}</h1>

                            {product.estoque <= 5 && product.estoque > 0 && (
                                <span className="badge-urgency mb-4 inline-block">🔥 Últimas {product.estoque} unidades!</span>
                            )}

                            <p className="text-4xl font-black text-gradient mb-6">R$ {product.current_price || product.preco}</p>

                            <div className="text-gray-400 mb-8">
                                <p>{product.descricao || 'Peça exclusiva da coleção GBlack. Design premium e acabamento impecável.'}</p>
                            </div>

                            <div className="flex items-center space-x-4 mb-8">
                                <div className="flex items-center border border-[#333] rounded-lg bg-[#1a1a1a]">
                                    <button
                                        className="px-4 py-3 hover:bg-[#333] text-white transition"
                                        onClick={() => setQuantity(Math.max(1, quantity - 1))}
                                    >-</button>
                                    <span className="px-6 font-bold text-white">{quantity}</span>
                                    <button
                                        className="px-4 py-3 hover:bg-[#333] text-white transition"
                                        onClick={() => setQuantity(quantity + 1)}
                                    >+</button>
                                </div>

                                <button
                                    onClick={addToCart}
                                    disabled={product.estoque === 0}
                                    className="flex-1 btn-primary py-4 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    <ShoppingCart size={20} className="mr-2" />
                                    {product.estoque > 0 ? 'Adicionar ao Carrinho' : 'Esgotado'}
                                </button>
                            </div>

                            <div className="border-t border-[#333] pt-6 space-y-2 text-sm text-gray-500">
                                <p className="flex items-center gap-2">✓ Pagamento 100% seguro</p>
                                <p className="flex items-center gap-2">✓ Envio em até 24h</p>
                                <p className="flex items-center gap-2">✓ Troca grátis em 30 dias</p>
                            </div>
                        </div>
                    </div>

                    {/* Related Products */}
                    {relatedProducts.length > 0 && (
                        <div className="mt-16">
                            <h2 className="text-2xl font-bold text-white mb-6">Você também pode gostar</h2>
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                                {relatedProducts.map((p) => (
                                    <Link key={p.id} to={`/product/${p.id}`} className="card-dark block group">
                                        <div className="h-48 overflow-hidden">
                                            {p.img_prod_url ? (
                                                <img src={p.img_prod_url} alt={p.nome} className="w-full h-full object-cover group-hover:scale-110 transition duration-500" />
                                            ) : (
                                                <div className="w-full h-full flex items-center justify-center text-gray-500">Sem Imagem</div>
                                            )}
                                        </div>
                                        <div className="p-4">
                                            <h3 className="font-semibold mb-1 truncate text-white">{p.nome}</h3>
                                            <p className="text-[#d4af37] font-bold">R$ {p.preco}</p>
                                        </div>
                                    </Link>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Sticky Buy Button */}
            <div className="fixed bottom-0 left-0 right-0 glass border-t border-[#333] p-4 z-40">
                <div className="container mx-auto flex items-center justify-between">
                    <div>
                        <p className="font-bold text-lg text-white">{product.nome}</p>
                        <p className="text-2xl font-black text-gradient">R$ {product.current_price || product.preco}</p>
                    </div>
                    <button
                        onClick={addToCart}
                        disabled={product.estoque === 0}
                        className="btn-primary py-3 px-8 flex items-center disabled:opacity-50"
                    >
                        <ShoppingCart size={20} className="mr-2" />
                        Comprar Agora
                    </button>
                </div>
            </div>
        </>
    );
};

export default ProductDetail;
