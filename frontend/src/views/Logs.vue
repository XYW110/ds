<template>
  <div class="logs-page">
    <div class="page-header">
      <h1>日志中心</h1>
      <div class="header-actions">
        <el-switch v-model="enableSSE" active-text="实时模式（SSE）" inactive-text="普通模式" @change="store.toggleSSE" />
        <el-button type="primary" :loading="store.loading" @click="store.fetchLogs">刷新</el-button>
      </div>
    </div>

    <el-alert v-if="store.sseConnected" type="success" title="已启用实时模式，自动接收新日志" show-icon class="mb-16" />
    <el-alert v-if="store.error" type="error" :title="store.error" show-icon class="mb-16" />

    <el-card class="filter-card" shadow="never">
      <el-form inline>
        <el-form-item label="日志级别">
          <el-select v-model="levelFilter" placeholder="全部级别" clearable style="width: 140px">
            <el-option label="DEBUG" value="DEBUG" />
            <el-option label="INFO" value="INFO" />
            <el-option label="WARNING" value="WARNING" />
            <el-option label="ERROR" value="ERROR" />
            <el-option label="CRITICAL" value="CRITICAL" />
          </el-select>
        </el-form-item>
        <el-form-item label="日志类型">
          <el-select v-model="typeFilter" placeholder="全部类型" clearable style="width: 140px">
            <el-option label="系统日志" value="system" />
            <el-option label="交易日志" value="trade" />
          </el-select>
        </el-form-item>
        <el-form-item label="关键字">
          <el-input v-model="keywordFilter" placeholder="搜索日志内容" clearable style="width: 200px" />
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker v-model="timeRange" type="datetimerange" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" value-format="YYYY-MM-DDTHH:mm:ss" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="applyFilters">应用过滤</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-table :data="store.logs" v-loading="store.loading" stripe height="640" style="margin-top: 16px">
      <el-table-column prop="level" label="级别" width="100">
        <template #default="{ row }">
          <el-tag :type="getLevelTagType(row.level)" size="small">{{ row.level }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="type" label="类型" width="100">
        <template #default="{ row }">
          <el-tag :type="row.type === 'trade' ? 'warning' : 'info'" size="small">{{ row.type === 'trade' ? '交易' : '系统' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="timestamp" label="时间" width="180">
        <template #default="{ row }">
          {{ formatTime(row.timestamp) }}
        </template>
      </el-table-column>
      <el-table-column prop="message" label="日志内容" min-width="400" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button size="small" @click="showDetail(row)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-wrapper">
      <el-pagination
        v-model:current-page="store.page"
        v-model:page-size="store.pageSize"
        :page-sizes="[50, 100, 200, 500]"
        layout="total, sizes, prev, pager, next"
        :total="store.total"
        @size-change="store.fetchLogs"
        @current-change="store.fetchLogs"
      />
    </div>

    <el-dialog v-model="dialogVisible" title="日志详情" width="640px" :destroy-on-close="true">
      <el-descriptions border>
        <el-descriptions-item label="ID">{{ selectedLog?.id ?? '-' }}</el-descriptions-item>
        <el-descriptions-item label="级别">
          <el-tag :type="getLevelTagType(selectedLog?.level)">{{ selectedLog?.level ?? '-' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="类型">
          <el-tag :type="selectedLog?.type === 'trade' ? 'warning' : 'info'">{{ selectedLog?.type === 'trade' ? '交易' : '系统' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="时间">{{ formatTime(selectedLog?.timestamp ?? '') }}</el-descriptions-item>
        <el-descriptions-item label="来源">{{ selectedLog?.source ?? '-' }}</el-descriptions-item>
        <el-descriptions-item label="Trace ID">{{ selectedLog?.trace_id ?? '-' }}</el-descriptions-item>
      </el-descriptions>
      <el-divider />
      <el-descriptions border>
        <el-descriptions-item label="日志内容" style="white-space: pre-wrap">
          {{ selectedLog?.message ?? '-' }}
        </el-descriptions-item>
      </el-descriptions>
      <el-alert v-if="!selectedLog" type="warning" title="未选择日志" show-icon />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import dayjs from 'dayjs'
import { useLogStore } from '@/stores/logs'
import type { LogEntry } from '@/api/types'

const store = useLogStore()
const dialogVisible = ref(false)
const selectedLog = ref<LogEntry | null>(null)

const enableSSE = computed(() => store.useSSE)
const levelFilter = ref<string | null>(store.filters.level)
const typeFilter = ref<string | null>(store.filters.type)
const keywordFilter = ref<string | null>(store.filters.keyword)
const timeRange = ref<[string, string] | null>(store.filters.fromTime && store.filters.toTime ? [store.filters.fromTime, store.filters.toTime] : null)

const formatTime = (value: string) => dayjs(value).format('YYYY-MM-DD HH:mm:ss')
const getLevelTagType = (level?: string) => {
  switch (level) {
    case 'DEBUG': return ''
    case 'INFO': return 'success'
    case 'WARNING': return 'warning'
    case 'ERROR':
    case 'CRITICAL': return 'danger'
    default: return 'info'
  }
}

const applyFilters = () => {
  store.updateFilter('level', levelFilter.value ?? null)
  store.updateFilter('type', typeFilter.value ?? null)
  store.updateFilter('keyword', keywordFilter.value ?? null)
  if (timeRange.value && timeRange.value.length === 2) {
    store.updateFilter('fromTime', timeRange.value[0] ?? null)
    store.updateFilter('toTime', timeRange.value[1] ?? null)
  } else {
    store.updateFilter('fromTime', null)
    store.updateFilter('toTime', null)
  }
}

const resetFilters = () => {
  levelFilter.value = null
  typeFilter.value = null
  keywordFilter.value = null
  timeRange.value = null
  applyFilters()
}

const showDetail = (log: LogEntry) => {
  selectedLog.value = log
  dialogVisible.value = true
}

watch(enableSSE, (value) => {
  store.toggleSSE(value)
})

onMounted(() => {
  store.fetchLogs()
})

onBeforeUnmount(() => {
  store.toggleSSE(false)
})
</script>

<style scoped>
.logs-page {
  padding: 24px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.mb-16 {
  margin-bottom: 16px;
}

.filter-card {
  margin-bottom: 16px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>
