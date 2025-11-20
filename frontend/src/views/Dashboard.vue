<template>
  <div class="dashboard">
    <div class="header">
      <h1>交易控制台仪表盘</h1>
      <div class="actions">
        <el-button :loading="store.loading" type="primary" @click="handleRefresh">
          刷新数据
        </el-button>
        <span class="timestamp" v-if="store.lastUpdated">上次更新：{{ formatTime(store.lastUpdated) }}</span>
      </div>
    </div>

    <el-alert v-if="store.error" type="error" show-icon :title="store.error" class="alert" />

    <el-row :gutter="16">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="card-title">交易引擎</div>
          <div class="card-value" :class="{ running: store.summary?.engine.running }">
            {{ store.summary?.engine.running ? '运行中' : '已停止' }}
          </div>
          <div class="card-desc">状态：{{ store.summary?.engine.status ?? '-' }}</div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card shadow="hover">
          <div class="card-title">信号总数</div>
          <div class="card-value">{{ store.summary?.signals.total_count ?? '-' }}</div>
          <div class="card-desc">最新信号：{{ store.summary?.signals.recent?.length ?? 0 }} 条</div>
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card shadow="hover">
          <div class="card-title">日限额使用</div>
          <div class="card-value">
            {{ store.summary?.daily_limit.used ?? '-' }} / {{ store.summary?.daily_limit.limit_usdt ?? '-' }}
          </div>
          <el-progress
            :percentage="store.summary?.daily_limit.usage_pct ?? 0"
            :stroke-width="16"
            status="success"
          />
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card shadow="hover">
          <div class="card-title">剩余额度</div>
          <div class="card-value">{{ store.summary?.daily_limit.remaining ?? '-' }}</div>
          <div class="card-desc">可用 USDT</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="signals-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>最新信号</span>
          <small>实时跟踪最近信号变化</small>
        </div>
      </template>
      <el-empty v-if="!store.summary?.signals.recent?.length" description="暂无信号" />
      <el-timeline v-else>
        <el-timeline-item
          v-for="(signal, index) in store.summary.signals.recent"
          :key="index"
          :timestamp="formatSignalTime(signal.timestamp)"
        >
          <div class="signal-item">
            <div class="signal-symbol">{{ signal.symbol || '未知' }}</div>
            <div class="signal-details">{{ signal.type }} · 信心 {{ signal.confidence ?? '-' }}</div>
          </div>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue'
import dayjs from 'dayjs'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()
let timer: number | null = null

const handleRefresh = async () => {
  await store.fetchSummary()
}

const formatTime = (time: string) => dayjs(time).format('YYYY-MM-DD HH:mm:ss')
const formatSignalTime = (time?: string) => (time ? dayjs(time).format('HH:mm:ss') : '-')

onMounted(async () => {
  await handleRefresh()
  timer = window.setInterval(handleRefresh, store.pollingInterval)
})

onBeforeUnmount(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
.dashboard {
  padding: 24px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.timestamp {
  color: #6b7280;
}

.alert {
  margin-bottom: 16px;
}

.card-title {
  font-size: 14px;
  color: #6b7280;
}

.card-value {
  font-size: 28px;
  font-weight: bold;
  margin-top: 8px;
}

.card-value.running {
  color: #10b981;
}

.card-desc {
  margin-top: 4px;
  color: #9ca3af;
}

.signals-card {
  margin-top: 24px;
}

.card-header {
  display: flex;
  flex-direction: column;
}

.signal-item {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.signal-symbol {
  font-weight: 600;
}

.signal-details {
  color: #6b7280;
}
</style>
