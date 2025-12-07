import React, { useEffect, useState } from 'react';
import api from '../../api';
import { Plus, Edit, Trash2, X, Save } from 'lucide-react';

const AdminProducts = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const [currentProduct, setCurrentProduct] = useState(null);
    const [formData, setFormData] = useState({
        nome: '',
        descricao: '',
        preco: '',
        tipo: 'R',
        estoque: '',
        is_available: true,
        img_prod: null
    });

    useEffect(() => {
        fetchProducts();
    }, []);

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

    const handleInputChange = (e) => {
        const { name, value, type, checked, files } = e.target;
        if (type === 'file') {
            setFormData(prev => ({ ...prev, [name]: files[0] }));
        } else {
            setFormData(prev => ({
                ...prev,
                [name]: type === 'checkbox' ? checked : value
            }));
        }
    };

    const startEdit = (product) => {
        setCurrentProduct(product);
        setFormData({
            nome: product.nome,
            descricao: product.descricao || '',
            preco: product.preco,
            tipo: product.tipo,
            estoque: product.estoque,
            is_available: product.is_available,
            img_prod: null
        });
        setIsEditing(true);
    };

    const startCreate = () => {
        setCurrentProduct(null);
        setFormData({
            nome: '',
            descricao: '',
            preco: '',
            tipo: 'R',
            estoque: '',
            is_available: true,
            img_prod: null
        });
        setIsEditing(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const data = new FormData();
        data.append('nome', formData.nome);
        data.append('descricao', formData.descricao);
        data.append('preco', formData.preco);
        data.append('tipo', formData.tipo);
        data.append('estoque', formData.estoque);
        data.append('is_available', formData.is_available);
        if (formData.img_prod) {
            data.append('img_prod', formData.img_prod);
        }

        try {
            if (currentProduct) {
                await api.patch(`products/${currentProduct.id}/`, data, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
            } else {
                await api.post('products/', data, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
            }
            setIsEditing(false);
            fetchProducts();
        } catch (error) {
            console.error('Error saving product:', error);
            alert('Erro ao salvar produto');
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Tem certeza que deseja excluir este produto?')) {
            try {
                await api.delete(`products/${id}/`);
                fetchProducts();
            } catch (error) {
                console.error('Error deleting product:', error);
            }
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <div className="flex justify-between items-center mb-8">
                <h1 className="text-3xl font-bold">Gerenciar Produtos</h1>
                <button
                    onClick={startCreate}
                    className="bg-black text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-gray-800 transition"
                >
                    <Plus size={20} />
                    <span>Novo Produto</span>
                </button>
            </div>

            {isEditing && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center p-4 z-50">
                    <div className="bg-white rounded-xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                        <div className="flex justify-between items-center mb-6">
                            <h2 className="text-2xl font-bold">{currentProduct ? 'Editar Produto' : 'Novo Produto'}</h2>
                            <button onClick={() => setIsEditing(false)} className="text-gray-500 hover:text-black">
                                <X size={24} />
                            </button>
                        </div>

                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Nome</label>
                                <input
                                    name="nome"
                                    value={formData.nome}
                                    onChange={handleInputChange}
                                    required
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Descrição</label>
                                <textarea
                                    name="descricao"
                                    value={formData.descricao}
                                    onChange={handleInputChange}
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                                />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Preço</label>
                                    <input
                                        name="preco"
                                        type="number"
                                        step="0.01"
                                        value={formData.preco}
                                        onChange={handleInputChange}
                                        required
                                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Estoque</label>
                                    <input
                                        name="estoque"
                                        type="number"
                                        value={formData.estoque}
                                        onChange={handleInputChange}
                                        required
                                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                                    />
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Tipo</label>
                                    <select
                                        name="tipo"
                                        value={formData.tipo}
                                        onChange={handleInputChange}
                                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                                    >
                                        <option value="R">Relógio</option>
                                        <option value="A">Acessório</option>
                                        <option value="V">Vestuário</option>
                                    </select>
                                </div>
                                <div className="flex items-center mt-6">
                                    <input
                                        name="is_available"
                                        type="checkbox"
                                        checked={formData.is_available}
                                        onChange={handleInputChange}
                                        className="h-4 w-4 text-black border-gray-300 rounded"
                                    />
                                    <label className="ml-2 block text-sm text-gray-900">Disponível</label>
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Imagem do Produto</label>
                                <input
                                    name="img_prod"
                                    type="file"
                                    onChange={handleInputChange}
                                    className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-gray-50 file:text-gray-700 hover:file:bg-gray-100"
                                />
                            </div>

                            <div className="flex justify-end space-x-3 pt-4">
                                <button
                                    type="button"
                                    onClick={() => setIsEditing(false)}
                                    className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                                >
                                    Cancelar
                                </button>
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-black text-white rounded-md hover:bg-gray-800 flex items-center space-x-2"
                                >
                                    <Save size={18} />
                                    <span>Salvar</span>
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            <div className="bg-white rounded-xl shadow-sm overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Produto</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Preço</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estoque</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {products.map((product) => (
                            <tr key={product.id}>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="flex items-center">
                                        <div className="h-10 w-10 flex-shrink-0">
                                            {product.img_prod_url ? (
                                                <img className="h-10 w-10 rounded-full object-cover" src={product.img_prod_url} alt="" />
                                            ) : (
                                                <div className="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-xs">N/A</div>
                                            )}
                                        </div>
                                        <div className="ml-4">
                                            <div className="text-sm font-medium text-gray-900">{product.nome}</div>
                                            <div className="text-sm text-gray-500">{product.tipo === 'R' ? 'Relógio' : product.tipo === 'A' ? 'Acessório' : 'Vestuário'}</div>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    R$ {product.preco}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {product.estoque}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${product.is_available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                        {product.is_available ? 'Ativo' : 'Inativo'}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    <button onClick={() => startEdit(product)} className="text-indigo-600 hover:text-indigo-900 mr-4">
                                        <Edit size={18} />
                                    </button>
                                    <button onClick={() => handleDelete(product.id)} className="text-red-600 hover:text-red-900">
                                        <Trash2 size={18} />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AdminProducts;
