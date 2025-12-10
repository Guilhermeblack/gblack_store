import React, { useEffect, useState } from 'react';
import api from '../api';
import { Link } from 'react-router-dom';

const Feed = () => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchFeed = async () => {
            try {
                const response = await api.get('feed/');
                setPosts(response.data.filter(post => post.is_published));
            } catch (error) {
                console.error('Error fetching feed:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchFeed();
    }, []);

    if (loading) return (
        <div className="flex justify-center items-center h-screen bg-[#0a0a0a]">
            <div className="animate-pulse text-[#d4af37]">Carregando feed...</div>
        </div>
    );

    return (
        <div className="bg-[#0a0a0a] min-h-screen py-8">
            <div className="container mx-auto px-4 max-w-3xl">
                <h1 className="text-4xl font-bold mb-8 text-center text-white">
                    Feed de <span className="text-gradient">Novidades</span>
                </h1>

                <div className="space-y-8">
                    {posts.length === 0 ? (
                        <p className="text-center text-gray-500">Nenhuma novidade por enquanto.</p>
                    ) : (
                        posts.map((post) => (
                            <div key={post.id} className="card-dark">
                                {post.image_url && (
                                    <img
                                        src={post.image_url}
                                        alt={post.title}
                                        className="w-full h-64 object-cover"
                                    />
                                )}
                                <div className="p-6">
                                    <div className="text-sm text-[#d4af37] mb-2">
                                        {new Date(post.scheduled_date).toLocaleDateString('pt-BR')}
                                    </div>
                                    <h2 className="text-2xl font-bold mb-3 text-white">{post.title}</h2>
                                    <div className="text-gray-400 whitespace-pre-line mb-4">
                                        {post.content}
                                    </div>

                                    {/* Linked Products */}
                                    {post.products && post.products.length > 0 && (
                                        <div className="border-t border-[#333] pt-4 mt-4">
                                            <p className="text-sm text-gray-500 mb-3">Produtos relacionados:</p>
                                            <div className="flex gap-4 overflow-x-auto pb-2">
                                                {post.products.map((product) => (
                                                    <Link
                                                        key={product.id}
                                                        to={`/product/${product.id}`}
                                                        className="flex-shrink-0 w-32 group"
                                                    >
                                                        <div className="bg-[#1a1a1a] rounded-lg overflow-hidden">
                                                            {product.img_prod_url ? (
                                                                <img
                                                                    src={product.img_prod_url}
                                                                    alt={product.nome}
                                                                    className="w-full h-32 object-cover group-hover:scale-110 transition"
                                                                />
                                                            ) : (
                                                                <div className="w-full h-32 flex items-center justify-center text-gray-500 text-xs">
                                                                    Sem imagem
                                                                </div>
                                                            )}
                                                            <div className="p-2">
                                                                <p className="text-white text-xs truncate">{product.nome}</p>
                                                                <p className="text-[#d4af37] text-sm font-bold">R$ {product.preco}</p>
                                                            </div>
                                                        </div>
                                                    </Link>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};

export default Feed;
