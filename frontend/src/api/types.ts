export type UserRole = 'admin' | 'user'

export interface LoginRequest {
  token: string
}

export interface LoginResponse {
  token: string
  role: UserRole
  expires_at: string
}

export interface ApiError {
  message: string
  code?: string
}

export interface StatusSummary {
  timestamp: string
  engine: {
    id: string
    status: string
    running: boolean
    config: Record<string, unknown>
  }
  signals: {
    total_count: number
    recent: Array<Record<string, unknown>>
  }
  daily_limit: {
    limit_usdt: number
    used: number
    remaining: number
    usage_pct: number
  }
  stats: {
    order_stats: Record<string, unknown>
    frequency_stats: Record<string, unknown>
  }
  error?: string
}

export interface LogEntry {
  id: string
  timestamp: string
  level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL'
  type: 'system' | 'trade'
  message: string
  source?: string
  trace_id?: string
}

export interface LogResponse {
  logs: LogEntry[]
  total: number
  page: number
  page_size: number
}

export interface TokenInfo {
  id: string
  token_preview: string
  role: UserRole
  created_at: string
  created_by: string
  expires_at: string
  is_active: boolean
  label: string
}

export interface CreateTokenRequest {
  label: string
  role: UserRole
  expires_days: number
}

export interface CreateTokenResponse {
  token: string
  token_info: TokenInfo
}
