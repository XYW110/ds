import { defineStore } from 'pinia'
import apiClient from '@/api/client'
import type { TokenInfo, CreateTokenRequest, CreateTokenResponse } from '@/api/types'

interface UserState {
  tokens: TokenInfo[]
  loading: boolean
  actionLoading: boolean
  error: string | null
  dialogVisible: boolean
  generatedToken: { token: string; preview: string } | null
}

export const useUserStore = defineStore('users', {
  state: (): UserState => ({
    tokens: [],
    loading: false,
    actionLoading: false,
    error: null,
    dialogVisible: false,
    generatedToken: null
  }),
  actions: {
    async fetchTokens() {
      this.loading = true
      this.error = null
      try {
        const { data } = await apiClient.get<{ tokens: TokenInfo[] }>('/auth/tokens?v=2')
        this.tokens = data.tokens
      } catch (error: unknown) {
        this.error = error instanceof Error ? error.message : '加载 Token 失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    async createToken(payload: CreateTokenRequest) {
      this.actionLoading = true
      this.error = null
      try {
        const { data } = await apiClient.post<CreateTokenResponse>('/auth/token', payload)
        this.generatedToken = { token: data.token, preview: data.token_info.token_preview }
        this.dialogVisible = true
        await this.fetchTokens()
        return data
      } catch (error: unknown) {
        this.error = error instanceof Error ? error.message : '创建 Token 失败'
        throw error
      } finally {
        this.actionLoading = false
      }
    },

    async revokeToken(tokenId: string) {
      this.actionLoading = true
      this.error = null
      try {
        await apiClient.post('/auth/revoke', { token_id: tokenId })
        await this.fetchTokens()
      } catch (error: unknown) {
        this.error = error instanceof Error ? error.message : '吊销 Token 失败'
        throw error
      } finally {
        this.actionLoading = false
      }
    }
  }
})
