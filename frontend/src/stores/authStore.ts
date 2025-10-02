import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { api } from '../services/api';

interface User {
  id: string;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  role: string;
  status: string;
  company?: {
    id: string;
    name: string;
  };
}

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
}

interface AuthActions {
  login: (email: string, password: string, deviceInfo?: any) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
  clearError: () => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState & AuthActions>()(
  persist(
    (set, get) => ({
      // State
      isAuthenticated: false,
      user: null,
      token: null,
      isLoading: false,
      error: null,

      // Actions
      login: async (email: string, password: string, deviceInfo?: any) => {
        set({ isLoading: true, error: null });
        
        try {
          const response = await api.post('/auth/login', {
            email,
            password,
            device_info: deviceInfo,
          });

          const { user, tokens } = response.data.data;
          
          set({
            isAuthenticated: true,
            user,
            token: tokens.access_token,
            isLoading: false,
            error: null,
          });

          // Set default authorization header
          api.defaults.headers.common['Authorization'] = `Bearer ${tokens.access_token}`;
        } catch (error: any) {
          set({
            isAuthenticated: false,
            user: null,
            token: null,
            isLoading: false,
            error: error.response?.data?.error?.message || 'Login failed',
          });
          throw error;
        }
      },

      logout: () => {
        set({
          isAuthenticated: false,
          user: null,
          token: null,
          error: null,
        });
        
        // Clear authorization header
        delete api.defaults.headers.common['Authorization'];
      },

      checkAuth: async () => {
        const { token } = get();
        
        if (!token) {
          set({ isAuthenticated: false, user: null });
          return;
        }

        set({ isLoading: true });
        
        try {
          // Set authorization header
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          
          const response = await api.get('/auth/profile');
          const { user } = response.data.data;
          
          set({
            isAuthenticated: true,
            user,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          set({
            isAuthenticated: false,
            user: null,
            token: null,
            isLoading: false,
            error: error.response?.data?.error?.message || 'Authentication failed',
          });
          
          // Clear authorization header
          delete api.defaults.headers.common['Authorization'];
        }
      },

      clearError: () => {
        set({ error: null });
      },

      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        isAuthenticated: state.isAuthenticated,
        user: state.user,
        token: state.token,
      }),
    }
  )
);