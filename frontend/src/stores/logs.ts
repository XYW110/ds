import { defineStore } from 'pinia'
import apiClient from '@/api/client'
import type { LogEntry, LogResponse } from '@/api/types'

class LogSSEManager {
  private eventSource: EventSource | null = null
  private store: ReturnType<typeof useLogStore> | null = null

  connect(store: ReturnType<typeof useLogStore>) {
    this.store = store
    if (this.eventSource) {
      this.disconnect()
    }

    this.eventSource = new EventSource('/api/logs/stream')

    this.eventSource.addEventListener('open', () => {
      if (this.store) {
        this.store.sseConnected = true
      }
    })

    this.eventSource.addEventListener('message', (event) => {
      if (this.store) {
        try {
          const log = JSON.parse(event.data) as LogEntry
          this.store.logs.unshift(log)
          if (this.store.logs.length > 1000) {
            this.store.logs = this.store.logs.slice(0, 1000)
          }
          this.store.total = Math.min(this.store.total + 1, 1000)
        } catch (e) {
          // ignore parse errors
        }
      }
    })

    this.eventSource.addEventListener('error', () => {
      if (this.store) {
        this.store.sseConnected = false
        this.store.error = 'SSE 连接已断开'
      }
      this.disconnect()
    })
  }

  disconnect() {
    if (this.eventSource) {
      this.eventSource.close()
      this.eventSource = null
    }
    if (this.store) {
      this.store.sseConnected = false
    }
  }
}

const sseManager = new LogSSEManager()

interface LogState {
  logs: LogEntry[]
  loading: boolean
  error: string | null
  total: number
  page: number
  pageSize: number
  filters: {
    level: string | null
    type: string | null
    keyword: string | null
    fromTime: string | null
    toTime: string | null
  }
  useSSE: boolean
  sseConnected: boolean
}

export const useLogStore = defineStore('logs', {
  state: (): LogState => ({
    logs: [],
    loading: false,
    error: null,
    total: 0,
    page: 1,
    pageSize: 50,
    filters: {
      level: null,
      type: null,
      keyword: null,
      fromTime: null,
      toTime: null
    },
    useSSE: false,
    sseConnected: false
  }),
  actions: {
    async fetchLogs() {
      if (this.useSSE) return

      this.loading = true
      this.error = null
      try {
        const params = new URLSearchParams()
        params.append('page', String(this.page))
        params.append('page_size', String(this.pageSize))
        if (this.filters.level) params.append('level', this.filters.level)
        if (this.filters.type) params.append('type', this.filters.type)
        if (this.filters.keyword) params.append('keyword', this.filters.keyword)
        if (this.filters.fromTime) params.append('from_time', this.filters.fromTime)
        if (this.filters.toTime) params.append('to_time', this.filters.toTime)

        const query = params.toString()
        const url = `/logs${query ? '?' + query : ''}`

        const { data } = await apiClient.get<LogResponse>(url)
        this.logs = data.logs
        this.total = data.total
        this.page = data.page
      } catch (error: unknown) {
        this.error = error instanceof Error ? error.message : '获取日志失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    updateFilter<K extends keyof LogState['filters']>(key: K, value: LogState['filters'][K]) {
      this.filters[key] = value
      this.page = 1
      this.fetchLogs()
    },

    setPage(page: number) {
      this.page = page
      this.fetchLogs()
    },

    toggleSSE(enabled: boolean) {
      this.useSSE = enabled
      if (enabled) {
        sseManager.connect(this)
      } else {
        sseManager.disconnect()
        this.fetchLogs()
      }
    }
  }
})
