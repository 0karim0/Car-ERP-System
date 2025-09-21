import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authService = {
  login: async (email, password) => {
    const response = await api.post('/api/auth/login/', { email, password });
    return response.data;
  },

  logout: async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (refreshToken) {
      await api.post('/api/auth/logout/', { refresh: refreshToken });
    }
  },

  register: async (userData) => {
    const response = await api.post('/api/auth/register/', userData);
    return response.data;
  },

  getProfile: async () => {
    const response = await api.get('/api/auth/profile/');
    return response.data;
  },

  updateProfile: async (userData) => {
    const response = await api.patch('/api/auth/profile/update/', userData);
    return response.data;
  },

  changePassword: async (passwordData) => {
    const response = await api.post('/api/auth/change-password/', passwordData);
    return response.data;
  },
};

export default api;
