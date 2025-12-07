import React, { useEffect, useState } from 'react';
import api from '../../api';
import { Plus, Edit, Trash2, X, Save, Image as ImageIcon } from 'lucide-react';

const AdminFeed = () => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const [currentPost, setCurrentPost] = useState(null);
    const [formData, setFormData] = useState({
        title: '',
        content: '',
        scheduled_date: '',
        is_published: false,
        image: null
    });

    useEffect(() => {
        fetchPosts();
    }, []);

    const fetchPosts = async () => {
        try {
            const response = await api.get('feed/');
            setPosts(response.data);
        } catch (error) {
            console.error('Error fetching feed posts:', error);
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

    const startEdit = (post) => {
        setCurrentPost(post);
        setFormData({
            title: post.title,
            content: post.content,
            scheduled_date: post.scheduled_date ? post.scheduled_date.slice(0, 16) : '', // Format for datetime-local
            is_published: post.is_published,
            image: null // Don't preload file input
        });
        setIsEditing(true);
    };

    const startCreate = () => {
        setCurrentPost(null);
        setFormData({
            title: '',
            content: '',
            scheduled_date: '',
            is_published: false,
            image: null
        });
        setIsEditing(true);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const data = new FormData();
        data.append('title', formData.title);
        data.append('content', formData.content);
        data.append('scheduled_date', formData.scheduled_date);
        data.append('is_published', formData.is_published);
        if (formData.image) {
            data.append('image', formData.image);
        }

        try {
            if (currentPost) {
                await api.patch(`feed/${currentPost.id}/`, data, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
            } else {
                await api.post('feed/', data, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
            }
            setIsEditing(false);
            fetchPosts();
        } catch (error) {
            console.error('Error saving post:', error);
            alert('Erro ao salvar post');
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Tem certeza que deseja excluir este post?')) {
            try {
                await api.delete(`feed/${id}/`);
                fetchPosts();
            } catch (error) {
                console.error('Error deleting post:', error);
            }
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <div className="flex justify-between items-center mb-8">
                <h1 className="text-3xl font-bold">Gerenciar Feed</h1>
                <button
                    onClick={startCreate}
                    className="bg-black text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-gray-800 transition"
                >
                    <Plus size={20} />
                    <span>Novo Post</span>
                </button>
            </div>

            {isEditing && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center p-4 z-50">
                    <div className="bg-white rounded-xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                        <div className="flex justify-between items-center mb-6">
                            <h2 className="text-2xl font-bold">{currentPost ? 'Editar Post' : 'Novo Post'}</h2>
                            <button onClick={() => setIsEditing(false)} className="text-gray-500 hover:text-black">
                                <X size={24} />
                            </button>
                        </div>

                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Título</label>
                                <input
                                    name="title"
                                    value={formData.title}
                                    onChange={handleInputChange}
                                    required
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Conteúdo</label>
                                <textarea
                                    name="content"
                                    value={formData.content}
                                    onChange={handleInputChange}
                                    required
                                    rows="4"
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Data de Publicação</label>
                                <input
                                    name="scheduled_date"
                                    type="datetime-local"
                                    value={formData.scheduled_date}
                                    onChange={handleInputChange}
                                    required
                                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Imagem</label>
                                <input
                                    name="image"
                                    type="file"
                                    onChange={handleInputChange}
                                    className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-gray-50 file:text-gray-700 hover:file:bg-gray-100"
                                />
                            </div>
                            <div className="flex items-center mt-4">
                                <input
                                    name="is_published"
                                    type="checkbox"
                                    checked={formData.is_published}
                                    onChange={handleInputChange}
                                    className="h-4 w-4 text-black border-gray-300 rounded"
                                />
                                <label className="ml-2 block text-sm text-gray-900">Publicado</label>
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
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Post</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {posts.map((post) => (
                            <tr key={post.id}>
                                <td className="px-6 py-4">
                                    <div className="flex items-center">
                                        <div className="h-10 w-10 flex-shrink-0">
                                            {post.image_url ? (
                                                <img className="h-10 w-10 rounded-full object-cover" src={post.image_url} alt="" />
                                            ) : (
                                                <div className="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-500">
                                                    <ImageIcon size={16} />
                                                </div>
                                            )}
                                        </div>
                                        <div className="ml-4">
                                            <div className="text-sm font-medium text-gray-900">{post.title}</div>
                                            <div className="text-sm text-gray-500 truncate max-w-xs">{post.content}</div>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {new Date(post.scheduled_date).toLocaleString()}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${post.is_published ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                                        {post.is_published ? 'Publicado' : 'Rascunho'}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    <button onClick={() => startEdit(post)} className="text-indigo-600 hover:text-indigo-900 mr-4">
                                        <Edit size={18} />
                                    </button>
                                    <button onClick={() => handleDelete(post.id)} className="text-red-600 hover:text-red-900">
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

export default AdminFeed;
