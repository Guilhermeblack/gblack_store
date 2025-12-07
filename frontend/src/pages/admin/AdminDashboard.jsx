import React, { useEffect, useState } from 'react';
import api from '../../api';
import { Package, ShoppingBag, DollarSign, Users } from 'lucide-react';

const AdminDashboard = () => {
    const [stats, setStats] = useState({
        products: 0,
        orders: 0,
        revenue: 0,
        customers: 0
    });

    useEffect(() => {
        const fetchStats = async () => {
            try {
                // In a real app, we would have a specific dashboard endpoint.
                // Here we will fetch lists and count them for simplicity.
                const [productsRes, ordersRes] = await Promise.all([
                    api.get('products/'),
                    api.get('orders/')
                ]);

                const products = productsRes.data;
                const orders = ordersRes.data;

                const revenue = orders.reduce((acc, order) => acc + parseFloat(order.total), 0);

                setStats({
                    products: products.length,
                    orders: orders.length,
                    revenue: revenue,
                    customers: 0 // We don't have a customers endpoint yet
                });
            } catch (error) {
                console.error('Error fetching dashboard stats:', error);
            }
        };

        fetchStats();
    }, []);

    const StatCard = ({ title, value, icon: Icon, color }) => (
        <div className="bg-white p-6 rounded-xl shadow-sm flex items-center space-x-4">
            <div className={`p-4 rounded-full ${color} text-white`}>
                <Icon size={24} />
            </div>
            <div>
                <p className="text-gray-500 text-sm">{title}</p>
                <h3 className="text-2xl font-bold">{value}</h3>
            </div>
        </div>
    );

    return (
        <div>
            <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Total de Vendas"
                    value={`R$ ${stats.revenue.toFixed(2)}`}
                    icon={DollarSign}
                    color="bg-green-500"
                />
                <StatCard
                    title="Pedidos"
                    value={stats.orders}
                    icon={ShoppingBag}
                    color="bg-blue-500"
                />
                <StatCard
                    title="Produtos"
                    value={stats.products}
                    icon={Package}
                    color="bg-purple-500"
                />
                {/* <StatCard 
                    title="Clientes" 
                    value={stats.customers} 
                    icon={Users} 
                    color="bg-orange-500" 
                /> */}
            </div>
        </div>
    );
};

export default AdminDashboard;
