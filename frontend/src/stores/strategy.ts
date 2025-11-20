import { defineStore } from 'pinia'
import apiClient from '@/api/client'

export interface StrategySummary {
  id: string
  name: string
  status: 'running' | 'stopped'
  parameters: Record<string, unknown>
  updated_at: string
}

interface StrategyState {
  list: StrategySummary[]
  selected: StrategySummary | null
  loading: boolean
  actionLoading: boolean
  error: string | null
  filterStatus: 'all' | 'running' | 'stopped'
}

export const useStrategyStore = defineStore('strategy', {
  state: (): StrategyState => ({
    list: [],
    selected: null,
    loading: false,
    actionLoading: false,
    error: null,
    filterStatus: 'all'
  }),
  getters: {
    filteredList: state => {
      if (state.filterStatus === 'all') return state.list
      return state.list.filter(item => item.status === state.filterStatus)
    }
  },
  actions: {
    async fetchStrategies() {
      this.loading = true
      this.error = null
      try {
        const { data } = await apiClient.get<{ strategies: StrategySummary[] }>('/strategy/list')
        this.list = data.strategies
      } catch (error: unknown) {
        this.error = error instanceof Error ? error.message : '加载策略失败'
      } finally {
        this.loading = false
      }
    },
    async fetchStrategyDetail(strategyId: string) {
      try {
        const { data } = await apiClient.get<StrategySummary>(`/strategy/${strategyId}`)
        this.selected = data
      } catch (error: unknown) {
        this.error = error instanceof Error ? error.message : '获取详情失败'
      }
    },
    async startStrategy(strategyId: string) {
      this.actionLoading = true
      try {
        await apiClient.post(`/strategy/${strategyId}/start`)
        await this.fetchStrategies()
        await this.fetchStrategyDetail(strategyId)
      } catch (error: unknown) {
        this.error = error instanceof Error ? error.message : '启动策略失败'
        throw error
      } finally {
        this.actionLoading = false
      }
    },
    async stopStrategy(strategyId: string) {
      this.actionLoading = true
      try {
        await apiClient.post(`/strategy/${strategyId}/stop`)
        await this.fetchStrategies()
        await this.fetchStrategyDetail(strategyId)
      } catch (error: unknown) {
        this.error = error instanceof Error ? error.message : '停止策略失败'
        throw error
      } finally {
        this.actionLoading = false
      }
    },
    async updateParams(strategyId: string, params: Record<string, unknown>) {
      this.actionLoading = true
      try {
        await apiClient.post(`/strategy/${strategyId}/params`, params)
        await this.fetchStrategies()
        await this.fetchStrategyDetail(strategyId)
      } catch (error: unknown) {
        this.error = error instanceof Error ? error.message : '更新参数失败'
        throw error
      } finally {
        this.actionLoading = false
      }
    }
  }
})
