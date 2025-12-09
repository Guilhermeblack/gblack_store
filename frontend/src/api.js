import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to include the auth token if available
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }

        // Guest ID logic
        let guestId = localStorage.getItem('guest_id');
        if (!guestId) {
            guestId = crypto.randomUUID();
            localStorage.setItem('guest_id', guestId);
        }
        config.headers['X-Guest-ID'] = guestId;

        return config;
    },
    (error) => Promise.reject(error)
);

export default api;
