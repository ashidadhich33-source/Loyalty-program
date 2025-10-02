import axios from 'axios';
import toast from 'react-hot-toast';

// Create axios instance
export const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add timestamp to prevent caching
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now(),
      };
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const { response } = error;
    
    if (response) {
      const { status, data } = response;
      
      switch (status) {
        case 401:
          // Unauthorized - redirect to login
          if (window.location.pathname !== '/login') {
            window.location.href = '/login';
          }
          break;
          
        case 403:
          toast.error('Access denied. You do not have permission to perform this action.');
          break;
          
        case 404:
          toast.error('Resource not found.');
          break;
          
        case 409:
          toast.error(data?.error?.message || 'Conflict. Resource already exists.');
          break;
          
        case 422:
          // Validation errors
          if (data?.error?.details) {
            const errors = Object.values(data.error.details).flat();
            toast.error(errors.join(', '));
          } else {
            toast.error(data?.error?.message || 'Validation failed.');
          }
          break;
          
        case 429:
          toast.error('Too many requests. Please try again later.');
          break;
          
        case 500:
          toast.error('Internal server error. Please try again later.');
          break;
          
        default:
          toast.error(data?.error?.message || 'An error occurred. Please try again.');
      }
    } else if (error.request) {
      // Network error
      toast.error('Network error. Please check your connection.');
    } else {
      // Other error
      toast.error('An unexpected error occurred.');
    }
    
    return Promise.reject(error);
  }
);

// API endpoints
export const endpoints = {
  // Auth
  auth: {
    login: '/auth/login',
    register: '/auth/register',
    logout: '/auth/logout',
    refresh: '/auth/refresh',
    profile: '/auth/profile',
    changePassword: '/auth/change-password',
  },
  
  // Users
  users: {
    list: '/users',
    create: '/users',
    get: (id: string) => `/users/${id}`,
    update: (id: string) => `/users/${id}`,
    delete: (id: string) => `/users/${id}`,
    restore: (id: string) => `/users/${id}/restore`,
    groups: (id: string) => `/users/${id}/groups`,
    permissions: (id: string) => `/users/${id}/permissions`,
    stats: '/users/stats',
  },
  
  // Companies
  companies: {
    list: '/companies',
    create: '/companies',
    get: (id: string) => `/companies/${id}`,
    update: (id: string) => `/companies/${id}`,
    delete: (id: string) => `/companies/${id}`,
    restore: (id: string) => `/companies/${id}/restore`,
    users: (id: string) => `/companies/${id}/users`,
    addUser: (id: string) => `/companies/${id}/users`,
    removeUser: (id: string, userId: string) => `/companies/${id}/users/${userId}`,
    stats: '/companies/stats',
    features: (id: string, feature: string) => `/companies/${id}/features/${feature}`,
    modules: (id: string, module: string) => `/companies/${id}/modules/${module}`,
  },
  
  // Health
  health: {
    basic: '/health',
    detailed: '/health/detailed',
  },
};

// API helper functions
export const apiHelpers = {
  // Pagination
  getPaginationParams: (page: number, limit: number) => ({
    page,
    limit,
  }),
  
  // Search
  getSearchParams: (search: string) => ({
    search,
  }),
  
  // Sorting
  getSortParams: (sortBy: string, sortOrder: 'ASC' | 'DESC' = 'DESC') => ({
    sort_by: sortBy,
    sort_order: sortOrder,
  }),
  
  // Filters
  getFilterParams: (filters: Record<string, any>) => {
    const params: Record<string, any> = {};
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params[key] = value;
      }
    });
    return params;
  },
  
  // Build query string
  buildQueryString: (params: Record<string, any>) => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        searchParams.append(key, String(value));
      }
    });
    return searchParams.toString();
  },
};

export default api;