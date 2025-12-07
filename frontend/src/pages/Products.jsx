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

    if (loading) return <div className="text-center py-10">Carregando produtos...</div>;

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold mb-8 text-center">Nossos Produtos</h1>

            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {products.map((product) => (
                    <Link to={`/products/${product.id}`} key={product.id} className="group">
                        <div className="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition">
                            <div className="aspect-square bg-gray-200 relative overflow-hidden">
                                {product.img_prod_url ? (
                                    <img
                                        src={product.img_prod_url}
                                        alt={product.nome}
                                        className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
                                    />
                                ) : (
                                    <div className="w-full h-full flex items-center justify-center text-gray-400">
                                        Sem imagem
                                    </div>
                                )}
                                {!product.is_available && (
                                    <div className="absolute top-2 right-2 bg-red-500 text-white text-xs px-2 py-1 rounded">
                                        Indisponível
                                    </div>
                                )}
                            </div>
                            <div className="p-4">
                                <h3 className="font-medium text-lg text-gray-900 group-hover:text-black transition">
                                    {product.nome}
                                </h3>
                                <p className="text-gray-500 text-sm mt-1 mb-3 line-clamp-2">{product.descricao}</p>
                                <div className="flex justify-between items-center">
                                    <span className="font-bold text-lg">R$ {product.preco}</span>
                                    <span className="text-sm text-gray-500">{product.tipo === 'R' ? 'Relógio' : product.tipo === 'A' ? 'Acessório' : 'Vestuário'}</span>
                                </div>
                            </div>
                        </div>
                    </Link>
                ))}
            </div>
        </div>
    );
};

export default Products;
