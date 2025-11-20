<template>
  <div class="strategy-page">
    <div class="page-header">
      <h1>策略管理</h1>
      <div class="header-actions">
        <el-select v-model="store.filterStatus" placeholder="状态过滤" size="small">
          <el-option label="全部" value="all" />
          <el-option label="运行中" value="running" />
          <el-option label="已停止" value="stopped" />
        </el-select>
        <el-button type="primary" :loading="store.loading" @click="store.fetchStrategies">
          刷新
        </el-button>
      </div>
    </div>

    <el-alert v-if="store.error" type="error" :title="store.error" show-icon class="mb-16" />

    <el-table :data="store.filteredList" stripe @row-click="handleRowClick">
      <el-table-column prop="name" label="策略名称" min-width="160" />
      <el-table-column prop="status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="row.status === 'running' ? 'success' : 'info'">
            {{ row.status === 'running' ? '运行中' : '已停止' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" label="更新时间" width="200">
        <template #default="{ row }">
          {{ formatTime(row.updated_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="260">
        <template #default="{ row }">
          <el-button
            size="small"
            type="success"
            :disabled="row.status === 'running' || !isAdmin"
            @click.stop="startStrategy(row.id)"
          >
            启动
          </el-button>
          <el-button
            size="small"
            type="warning"
            :disabled="row.status === 'stopped' || !isAdmin"
            @click.stop="stopStrategy(row.id)"
          >
            停止
          </el-button>
          <el-button size="small" @click.stop="openDetail(row.id)">
            详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-drawer v-model="drawerVisible" title="策略详情" size="50%" :destroy-on-close="true">
      <template v-if="store.selected">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="策略 ID">{{ store.selected.id }}</el-descriptions-item>
          <el-descriptions-item label="当前状态">
            <el-tag :type="store.selected.status === 'running' ? 'success' : 'info'">
              {{ store.selected.status === 'running' ? '运行中' : '已停止' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ formatTime(store.selected.updated_at) }}</el-descriptions-item>
        </el-descriptions>

        <el-alert
          v-if="!isAdmin"
          type="info"
          show-icon
          title="普通用户仅可查看，无法修改参数"
          class="mb-16"
        />

        <el-divider>参数配置</el-divider>
        <el-form :model="paramForm" label-width="120px">
          <el-form-item
            v-for="(value, key) in paramForm"
            :key="key"
            :label="key"
          >
            <el-input v-model="paramForm[key]" :disabled="!isAdmin" />
          </el-form-item>
        </el-form>

        <div class="form-actions">
          <el-button @click="resetParams" :disabled="!isAdmin">重置</el-button>
          <el-button type="primary" :loading="store.actionLoading" :disabled="!isAdmin" @click="saveParams">
            保存参数
          </el-button>
        </div>
      </template>
      <el-empty v-else description="请选择一条策略" />
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, computed, onMounted } from 'vue'
import dayjs from 'dayjs'
import { useStrategyStore } from '@/stores/strategy'
import { useAuthStore } from '@/stores/auth'

const store = useStrategyStore()
const auth = useAuthStore()
const drawerVisible = ref(false)
const paramForm = reactive<Record<string, any>>({})
const isAdmin = computed(() => auth.isAdmin)

const formatTime = (value: string) => dayjs(value).format('YYYY-MM-DD HH:mm:ss')

const handleRowClick = (row: { id: string }) => {
  openDetail(row.id)
}

const openDetail = async (strategyId: string) => {
  drawerVisible.value = true
  await store.fetchStrategyDetail(strategyId)
  resetParams()
}

const startStrategy = async (strategyId: string) => {
  if (!isAdmin.value) return
  await store.startStrategy(strategyId)
}

const stopStrategy = async (strategyId: string) => {
  if (!isAdmin.value) return
  await store.stopStrategy(strategyId)
}

const resetParams = () => {
  if (!store.selected) return
  Object.keys(paramForm).forEach(key => delete paramForm[key])
  Object.entries(store.selected.parameters || {}).forEach(([key, value]) => {
    paramForm[key] = value
  })
}

const saveParams = async () => {
  if (!store.selected || !isAdmin.value) return
  await store.updateParams(store.selected.id, { ...paramForm })
}

watch(() => store.selected?.parameters, () => {
  resetParams()
})

onMounted(() => {
  store.fetchStrategies()
})
</script>

<style scoped>
.strategy-page {
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
  gap: 12px;
}

.mb-16 {
  margin-bottom: 16px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}
</style>
