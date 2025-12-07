import React, { useEffect, useState } from 'react';
import api from '../api';
import { Link } from 'react-router-dom';

const Home = () => {
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

    if (loading) {
        return <div className="flex justify-center items-center h-screen">Loading...</div>;
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <section className="mb-12">
                <div className="bg-gray-900 text-white rounded-2xl p-8 md:p-16 text-center">
                    <h1 className="text-4xl md:text-6xl font-bold mb-4">Estilo e Atitude</h1>
                    <p className="text-xl mb-8 text-gray-300">Descubra a nova coleção GBlack.</p>
                    <Link to="/products" className="bg-white text-black px-8 py-3 rounded-full font-semibold hover:bg-gray-200 transition">
                        Ver Coleção
                    </Link>
                </div>
            </section>

            <h2 className="text-3xl font-bold mb-8 text-center">Destaques</h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
                {products.map((product) => (
                    <div key={product.id} className="bg-white rounded-xl shadow-sm hover:shadow-md transition overflow-hidden group">
                        <div className="relative aspect-square overflow-hidden bg-gray-100">
                            {product.img_prod_url ? (
                                <img
                                    src={product.img_prod_url}
                                    alt={product.nome}
                                    className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
                                />
                            ) : (
                                <div className="w-full h-full flex items-center justify-center text-gray-400">Sem Imagem</div>
                            )}
                        </div>
                        <div className="p-4">
                            <h3 className="font-semibold text-lg mb-1">{product.nome}</h3>
                            <p className="text-gray-500 text-sm mb-3">{product.tipo === 'R' ? 'Relógio' : product.tipo === 'A' ? 'Acessório' : 'Vestuário'}</p>
                            <div className="flex justify-between items-center">
                                <span className="font-bold text-lg">R$ {product.preco}</span>
                                <button className="bg-black text-white px-4 py-2 rounded-lg text-sm hover:bg-gray-800 transition">
                                    Ver Detalhes
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Home;
