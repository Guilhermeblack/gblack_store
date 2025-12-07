import React, { useEffect, useState } from 'react';
import api from '../api';

const Feed = () => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchFeed = async () => {
            try {
                const response = await api.get('feed/');
                // Filter only published posts if the API doesn't do it automatically for non-admins
                // Ideally the API should handle this, but for safety we can check here too if needed.
                // Assuming API returns all for now, we render what we get.
                setPosts(response.data.filter(post => post.is_published));
            } catch (error) {
                console.error('Error fetching feed:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchFeed();
    }, []);

    if (loading) return <div className="text-center py-10">Carregando feed...</div>;

    return (
        <div className="container mx-auto px-4 py-8 max-w-3xl">
            <h1 className="text-3xl font-bold mb-8 text-center">Feed de Novidades</h1>

            <div className="space-y-8">
                {posts.length === 0 ? (
                    <p className="text-center text-gray-500">Nenhuma novidade por enquanto.</p>
                ) : (
                    posts.map((post) => (
                        <div key={post.id} className="bg-white rounded-xl shadow-sm overflow-hidden">
                            {post.image_url && (
                                <img
                                    src={post.image_url}
                                    alt={post.title}
                                    className="w-full h-64 object-cover"
                                />
                            )}
                            <div className="p-6">
                                <div className="text-sm text-gray-500 mb-2">
                                    {new Date(post.scheduled_date).toLocaleDateString()}
                                </div>
                                <h2 className="text-2xl font-bold mb-3">{post.title}</h2>
                                <div className="prose max-w-none text-gray-700 whitespace-pre-line">
                                    {post.content}
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default Feed;
