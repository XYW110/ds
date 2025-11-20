import { defineStore } from 'pinia'
import apiClient from '@/api/client'
import type { LoginRequest, LoginResponse, UserRole } from '@/api/types'

interface AuthState {
  token: string | null
  role: UserRole | null
  loading: boolean
  error: string | null
}

const storageKey = 'auth_token'
const roleKey = 'auth_role'

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem(storageKey),
    role: (localStorage.getItem(roleKey) as UserRole | null) ?? null,
    loading: false,
    error: null
  }),
  getters: {
    isAuthenticated: state => Boolean(state.token),
    isAdmin: state => state.role === 'admin'
  },
  actions: {
    async login(payload: LoginRequest) {
      this.loading = true
      this.error = null
      try {
        const { data } = await apiClient.post<LoginResponse>('/auth/login', payload)
        this.token = data.token
        this.role = data.role
        localStorage.setItem(storageKey, data.token)
        localStorage.setItem(roleKey, data.role)
      } catch (error: unknown) {
        this.error = error instanceof Error ? error.message : '登录失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    logout() {
      this.token = null
      this.role = null
      localStorage.removeItem(storageKey)
      localStorage.removeItem(roleKey)
    }
  }
})
