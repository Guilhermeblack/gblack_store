import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

const Products = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await api.get('products/');
                setProducts(response.data);
            } catch (error) {
                console.error('Error fetching products:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);

    if (loading) return (
        <div className="flex justify-center items-center h-screen bg-[#0a0a0a]">
            <div className="animate-pulse text-[#d4af37]">Carregando produtos...</div>
        </div>
    );

    return (
        <div className="bg-[#0a0a0a] min-h-screen py-8">
            <div className="container mx-auto px-4">
                <h1 className="text-4xl font-bold mb-8 text-center text-white">
                    Nossos <span className="text-gradient">Produtos</span>
                </h1>

                <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {products.map((product) => (
                        <Link to={`/products/${product.id}`} key={product.id} className="group">
                            <div className="card-dark">
                                <div className="aspect-square relative overflow-hidden">
                                    {product.img_prod_url ? (
                                        <img
                                            src={product.img_prod_url}
                                            alt={product.nome}
                                            className="w-full h-full object-cover group-hover:scale-110 transition duration-500"
                                        />
                                    ) : (
                                        <div className="w-full h-full flex items-center justify-center bg-[#1a1a1a] text-gray-500">
                                            Sem imagem
                                        </div>
                                    )}
                                    {!product.is_available && (
                                        <div className="absolute top-2 right-2 bg-red-600 text-white text-xs px-2 py-1 rounded font-bold">
                                            Indisponível
                                        </div>
                                    )}
                                    {product.estoque <= 5 && product.estoque > 0 && (
                                        <span className="absolute top-2 left-2 badge-urgency">
                                            Últimas unidades!
                                        </span>
                                    )}
                                </div>
                                <div className="p-4">
                                    <p className="text-[#d4af37] text-xs font-semibold uppercase tracking-wider mb-1">
                                        {product.tipo === 'R' ? 'Relógio' : product.tipo === 'A' ? 'Acessório' : 'Vestuário'}
                                    </p>
                                    <h3 className="font-bold text-lg text-white group-hover:text-[#d4af37] transition truncate">
                                        {product.nome}
                                    </h3>
                                    <p className="text-gray-500 text-sm mt-1 mb-3 line-clamp-2">{product.descricao}</p>
                                    <div className="flex justify-between items-center">
                                        <span className="font-black text-xl text-white">R$ {product.current_price || product.preco}</span>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Products;
