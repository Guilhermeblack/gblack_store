import React, { useEffect, useState } from 'react';
import api from '../api';
import { Link } from 'react-router-dom';
import { Star, Truck, Shield, Clock, ChevronRight } from 'lucide-react';

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
        return (
            <div className="flex justify-center items-center h-screen bg-[#0a0a0a]">
                <div className="animate-pulse text-[#d4af37] text-xl">Carregando...</div>
            </div>
        );
    }

    return (
        <div className="bg-[#0a0a0a] min-h-screen">
            {/* Hero Section */}
            <section className="relative h-[80vh] flex items-center justify-center overflow-hidden">
                <div
                    className="absolute inset-0 bg-cover bg-center"
                    style={{ backgroundImage: 'url(/hero_banner.png)' }}
                >
                    <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-[#0a0a0a]"></div>
                </div>

                <div className="relative z-10 text-center px-4 max-w-4xl animate-fadeIn">
                    <span className="inline-block bg-[#d4af37] text-black text-sm font-bold px-4 py-1 rounded-full mb-6 uppercase tracking-wider">
                        🔥 Frete Grátis Hoje
                    </span>
                    <h1 className="text-5xl md:text-7xl font-black mb-6 leading-tight">
                        Vista-se para <span className="text-gradient">Dominar</span>
                    </h1>
                    <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-2xl mx-auto">
                        Acessórios exclusivos para quem não aceita o comum. Estilo que impõe respeito.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link to="/products" className="btn-primary flex items-center justify-center gap-2">
                            Ver Coleção <ChevronRight size={20} />
                        </Link>
                        <Link to="/feed" className="btn-secondary">
                            Novidades
                        </Link>
                    </div>
                </div>
            </section>

            {/* Social Proof */}
            <section className="py-8 border-y border-[#1a1a1a]">
                <div className="container mx-auto px-4">
                    <div className="flex flex-wrap justify-center gap-8 md:gap-16 text-center">
                        <div className="flex items-center gap-2">
                            <Star className="text-[#d4af37]" size={24} fill="#d4af37" />
                            <span className="text-gray-300"><strong className="text-white">1.500+</strong> Clientes Satisfeitos</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <Truck className="text-[#d4af37]" size={24} />
                            <span className="text-gray-300">Entrega para <strong className="text-white">Todo Brasil</strong></span>
                        </div>
                        <div className="flex items-center gap-2">
                            <Shield className="text-[#d4af37]" size={24} />
                            <span className="text-gray-300"><strong className="text-white">Pagamento Seguro</strong></span>
                        </div>
                        <div className="flex items-center gap-2">
                            <Clock className="text-[#d4af37]" size={24} />
                            <span className="text-gray-300">Envio em <strong className="text-white">24h</strong></span>
                        </div>
                    </div>
                </div>
            </section>

            {/* Products Grid */}
            <section className="py-16">
                <div className="container mx-auto px-4">
                    <div className="text-center mb-12">
                        <h2 className="text-4xl font-bold mb-4">Produtos em <span className="text-gradient">Destaque</span></h2>
                        <p className="text-gray-400 max-w-xl mx-auto">Peças selecionadas que elevam seu estilo a outro nível</p>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                        {products.slice(0, 8).map((product, index) => (
                            <div
                                key={product.id}
                                className="card-dark group animate-fadeIn"
                                style={{ animationDelay: `${index * 0.1}s` }}
                            >
                                <Link to={`/product/${product.id}`} className="relative aspect-square block overflow-hidden">
                                    {product.img_prod_url ? (
                                        <img
                                            src={product.img_prod_url}
                                            alt={product.nome}
                                            className="w-full h-full object-cover group-hover:scale-110 transition duration-500"
                                        />
                                    ) : (
                                        <div className="w-full h-full flex items-center justify-center bg-[#1a1a1a] text-gray-500">
                                            Sem Imagem
                                        </div>
                                    )}
                                    {product.estoque <= 5 && product.estoque > 0 && (
                                        <span className="absolute top-3 left-3 badge-urgency">
                                            Últimas {product.estoque} unidades!
                                        </span>
                                    )}
                                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-4">
                                        <span className="text-white font-bold">Ver Detalhes →</span>
                                    </div>
                                </Link>
                                <div className="p-4">
                                    <p className="text-[#d4af37] text-xs font-semibold uppercase tracking-wider mb-1">
                                        {product.tipo === 'R' ? 'Relógio' : product.tipo === 'A' ? 'Acessório' : 'Vestuário'}
                                    </p>
                                    <h3 className="font-bold text-lg mb-2 text-white group-hover:text-[#d4af37] transition truncate">
                                        {product.nome}
                                    </h3>
                                    <div className="flex justify-between items-center">
                                        <span className="text-2xl font-black text-white">
                                            R$ {product.current_price || product.preco}
                                        </span>
                                        <Link
                                            to={`/product/${product.id}`}
                                            className="bg-[#d4af37] text-black px-4 py-2 rounded-lg text-sm font-bold hover:bg-[#f0d060] transition"
                                        >
                                            Comprar
                                        </Link>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    {products.length > 8 && (
                        <div className="text-center mt-12">
                            <Link to="/products" className="btn-secondary inline-flex items-center gap-2">
                                Ver Todos os Produtos <ChevronRight size={20} />
                            </Link>
                        </div>
                    )}
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 bg-gradient-to-r from-[#1a1a1a] to-[#0a0a0a]">
                <div className="container mx-auto px-4 text-center">
                    <h2 className="text-4xl md:text-5xl font-black mb-6">
                        Pronto para <span className="text-gradient">se destacar</span>?
                    </h2>
                    <p className="text-gray-400 text-xl mb-8 max-w-2xl mx-auto">
                        Junte-se a mais de 1.500 clientes que já transformaram seu estilo
                    </p>
                    <Link to="/products" className="btn-primary inline-flex items-center gap-2 animate-pulse-gold">
                        Explorar Agora <ChevronRight size={20} />
                    </Link>
                </div>
            </section>
        </div>
    );
};

export default Home;
