import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';
import { ShoppingCart, ArrowLeft, X, ChevronLeft, ChevronRight } from 'lucide-react';

const ProductDetail = () => {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [relatedProducts, setRelatedProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [quantity, setQuantity] = useState(1);
    const [showCarousel, setShowCarousel] = useState(false);
    const [currentImageIndex, setCurrentImageIndex] = useState(0);

    // For demo purposes, we'll simulate multiple images
    const getProductImages = () => {
        if (!product) return [];
        // If product has multiple images, use them. Otherwise, use the main image.
        return product.img_prod_url ? [product.img_prod_url] : [];
    };

    useEffect(() => {
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

        fetchProduct();
    }, [id]);

    const addToCart = async () => {
        try {
            await api.post('cart/add_item/', {
                product_id: product.id,
                quantity: quantity
            });
            alert('Produto adicionado ao carrinho! Seu item está reservado.');
            window.dispatchEvent(new Event('cartUpdated'));
        } catch (error) {
            console.error('Error adding to cart:', error);
            alert(error.response?.data?.error || 'Erro ao adicionar ao carrinho.');
        }
    };

    const images = getProductImages();

    if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;
    if (!product) return <div className="text-center py-20">Produto não encontrado</div>;

    return (
        <>
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

            <div className="container mx-auto px-4 py-8 pb-24">
                <Link to="/" className="inline-flex items-center text-gray-600 hover:text-black mb-8">
                    <ArrowLeft size={20} className="mr-2" /> Voltar
                </Link>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                    <div
                        className="bg-white rounded-2xl overflow-hidden shadow-sm cursor-pointer hover:shadow-lg transition"
                        onClick={() => images.length > 0 && setShowCarousel(true)}
                    >
                        {product.img_prod_url ? (
                            <img src={product.img_prod_url} alt={product.nome} className="w-full h-full object-cover" />
                        ) : (
                            <div className="w-full h-96 flex items-center justify-center bg-gray-100 text-gray-400">Sem Imagem</div>
                        )}
                        {images.length > 0 && (
                            <div className="absolute bottom-2 right-2 bg-black/50 text-white px-2 py-1 rounded text-xs">
                                Clique para ampliar
                            </div>
                        )}
                    </div>

                    <div>
                        <h1 className="text-4xl font-bold mb-4">{product.nome}</h1>
                        <p className="text-3xl font-semibold text-green-600 mb-6">R$ {product.preco}</p>

                        <div className="prose text-gray-600 mb-8">
                            <p>{product.descricao || 'Produto de alta qualidade da coleção GBlack.'}</p>
                        </div>

                        <div className="flex items-center space-x-4 mb-8">
                            <div className="flex items-center border rounded-lg">
                                <button
                                    className="px-4 py-2 hover:bg-gray-100"
                                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                                >-</button>
                                <span className="px-4 font-medium">{quantity}</span>
                                <button
                                    className="px-4 py-2 hover:bg-gray-100"
                                    onClick={() => setQuantity(quantity + 1)}
                                >+</button>
                            </div>

                            <button
                                onClick={addToCart}
                                className="flex-1 bg-black text-white py-3 px-6 rounded-lg font-semibold hover:bg-gray-800 transition flex items-center justify-center"
                            >
                                <ShoppingCart size={20} className="mr-2" />
                                Adicionar ao Carrinho
                            </button>
                        </div>

                        <div className="border-t pt-6 text-sm text-gray-500">
                            <p>Categoria: {product.tipo === 'R' ? 'Relógio' : product.tipo === 'A' ? 'Acessório' : 'Vestuário'}</p>
                            <p>Estoque: {product.estoque > 0 ? `${product.estoque} unidades disponíveis` : <span className="text-red-500">Esgotado</span>}</p>
                        </div>
                    </div>
                </div>

                {/* Related Products */}
                {relatedProducts.length > 0 && (
                    <div className="mt-16">
                        <h2 className="text-2xl font-bold mb-6">Você também pode gostar</h2>
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                            {relatedProducts.map((p) => (
                                <Link key={p.id} to={`/product/${p.id}`} className="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition block">
                                    <div className="h-48 bg-gray-100">
                                        {p.img_prod_url ? (
                                            <img src={p.img_prod_url} alt={p.nome} className="w-full h-full object-cover" />
                                        ) : (
                                            <div className="w-full h-full flex items-center justify-center text-gray-400">Sem Imagem</div>
                                        )}
                                    </div>
                                    <div className="p-4">
                                        <h3 className="font-semibold mb-1 truncate">{p.nome}</h3>
                                        <p className="text-gray-900 font-bold">R$ {p.preco}</p>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    </div>
                )}
            </div>

            {/* Sticky Buy Button */}
            <div className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg p-4 z-40">
                <div className="container mx-auto flex items-center justify-between">
                    <div>
                        <p className="font-semibold text-lg">{product.nome}</p>
                        <p className="text-2xl font-bold text-green-600">R$ {product.preco}</p>
                    </div>
                    <button
                        onClick={addToCart}
                        className="bg-black text-white py-3 px-8 rounded-lg font-semibold hover:bg-gray-800 transition flex items-center"
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
