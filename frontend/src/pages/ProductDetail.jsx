import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';
import { ShoppingCart, ArrowLeft } from 'lucide-react';

const ProductDetail = () => {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [quantity, setQuantity] = useState(1);

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const response = await api.get(`products/${id}/`);
                setProduct(response.data);
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
            alert('Produto adicionado ao carrinho!');
        } catch (error) {
            console.error('Error adding to cart:', error);
            alert('Erro ao adicionar ao carrinho. Faça login para continuar.');
        }
    };

    if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;
    if (!product) return <div className="text-center py-20">Produto não encontrado</div>;

    return (
        <div className="container mx-auto px-4 py-8">
            <Link to="/" className="inline-flex items-center text-gray-600 hover:text-black mb-8">
                <ArrowLeft size={20} className="mr-2" /> Voltar
            </Link>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                <div className="bg-white rounded-2xl overflow-hidden shadow-sm">
                    {product.img_prod_url ? (
                        <img src={product.img_prod_url} alt={product.nome} className="w-full h-full object-cover" />
                    ) : (
                        <div className="w-full h-96 flex items-center justify-center bg-gray-100 text-gray-400">Sem Imagem</div>
                    )}
                </div>

                <div>
                    <h1 className="text-4xl font-bold mb-4">{product.nome}</h1>
                    <p className="text-2xl font-semibold mb-6">R$ {product.preco}</p>

                    <div className="prose text-gray-600 mb-8">
                        <p>{product.descricao}</p>
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
                        <p>Estoque: {product.estoque} unidades</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProductDetail;
