import { defineStore } from 'pinia'
import apiClient from '@/api/client'
import type { StatusSummary } from '@/api/types'

interface DashboardState {
  summary: StatusSummary | null
  loading: boolean
  error: string | null
  lastUpdated: string | null
  pollingInterval: number
}

export const useDashboardStore = defineStore('dashboard', {
  state: (): DashboardState => ({
    summary: null,
    loading: false,
    error: null,
    lastUpdated: null,
    pollingInterval: 8000
  }),
  actions: {
    async fetchSummary() {
      this.loading = true
      this.error = null
      try {
        const { data } = await apiClient.get<StatusSummary>('/status/summary')
        this.summary = data
        this.lastUpdated = data.timestamp
      } catch (error: unknown) {
        this.error = error instanceof Error ? error.message : '获取数据失败'
      } finally {
        this.loading = false
      }
    }
  }
})
