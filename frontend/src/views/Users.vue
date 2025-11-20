<template>
  <div class="users-page">
    <div class="page-header">
      <h1>用户 Token 管理</h1>
      <div class="header-actions">
        <el-button type="primary" @click="openCreateDialog" :loading="store.actionLoading">
          生成新 Token
        </el-button>
        <el-button @click="store.fetchTokens" :loading="store.loading">刷新</el-button>
      </div>
    </div>

    <!-- Only visible to admin -->
    <div v-if="!isAdmin" class="access-denied">
      <el-result icon="warning" title="权限不足" sub-title="此页面仅管理员可访问">
        <template #extra>
          <el-button type="primary" @click="$router.push('/dashboard')">返回仪表盘</el-button>
        </template>
      </el-result>
    </div>

    <div v-else>
      <el-alert v-if="store.error" type="error" :title="store.error" show-icon class="mb-16" />

      <el-table :data="store.tokens" v-loading="store.loading" stripe>
        <el-table-column prop="label" label="标签" min-width="160" />
        <el-table-column prop="token_preview" label="Token 预览" width="200" />
        <el-table-column prop="role" label="权限" width="100">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'info'">{{ row.role }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_by" label="创建人" width="150" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="expires_at" label="过期时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.expires_at) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'">
              {{ row.is_active ? '有效' : '已吊销' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-popconfirm title="确定要吊销此 Token 吗？" @confirm="revokeToken(row.id)">
              <template #reference>
                <el-button size="small" type="danger" :disabled="!row.is_active">
                  吊销
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- Create Token Dialog -->
    <el-dialog v-model="createDialogVisible" title="生成新 Token" width="520px" :destroy-on-close="true">
      <el-form :model="createForm" :rules="createRules" ref="createFormRef" label-width="100px">
        <el-form-item label="标签" prop="label">
          <el-input v-model="createForm.label" placeholder="用于识别令牌用途，如 '测试账户'" />
        </el-form-item>
        <el-form-item label="权限" prop="role">
          <el-select v-model="createForm.role" placeholder="选择权限" style="width: 100%">
            <el-option label="管理员" value="admin" />
            <el-option label="普通用户" value="user" />
          </el-select>
        </el-form-item>
        <el-form-item label="有效期" prop="expires_days">
          <el-input-number v-model="createForm.expires_days" :min="1" :max="365" />
          <span style="margin-left: 12px; color: #6b7280">天</span>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitCreate" :loading="store.actionLoading">
          生成
        </el-button>
      </template>
    </el-dialog>

    <!-- Show Generated Token Dialog -->
    <el-dialog v-model="store.dialogVisible" title="Token 生成成功" width="640px" :destroy-on-close="true">
      <el-result icon="success" title="Token 已生成" sub-title="请妥善保管，此 Token 只显示一次">
        <template #extra>
          <el-alert
            title="⚠️ 安全提示：Token 仅显示一次，请立即复制并妥善保管。如果丢失，需要重新生成。"
            type="warning"
            :closable="false"
            show-icon
            style="margin-bottom: 16px"
          />
          <el-descriptions border>
            <el-descriptions-item label="Token">{{ store.generatedToken?.token }}</el-descriptions-item>
            <el-descriptions-item label="预览">{{ store.generatedToken?.preview }}</el-descriptions-item>
          </el-descriptions>
          <el-button type="primary" @click="copyToken" style="margin-top: 16px">
            复制 Token
          </el-button>
        </template>
      </el-result>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/users'
import { useAuthStore } from '@/stores/auth'

const store = useUserStore()
const auth = useAuthStore()

const isAdmin = computed(() => auth.isAdmin)
const createDialogVisible = ref(false)
const createForm = ref({
  label: '',
  role: 'user' as 'admin' | 'user',
  expires_days: 30
})
const createFormRef = ref()

const createRules = {
  label: [{ required: true, message: '请输入标签', trigger: 'blur' }],
  role: [{ required: true, message: '请选择权限', trigger: 'change' }],
  expires_days: [{ required: true, message: '请输入有效期', trigger: 'blur' }]
}

const formatTime = (value: string) => dayjs(value).format('YYYY-MM-DD HH:mm:ss')

const openCreateDialog = () => {
  createForm.value = { label: '', role: 'user', expires_days: 30 }
  createDialogVisible.value = true
}

const submitCreate = async () => {
  try {
    await createFormRef.value.validate()
    await store.createToken(createForm.value)
    createDialogVisible.value = false
  } catch (e) {
    // validation or API error
  }
}

const revokeToken = async (tokenId: string) => {
  await store.revokeToken(tokenId)
  ElMessage.success('Token 已吊销')
}

const copyToken = async () => {
  if (!store.generatedToken) return
  try {
    await navigator.clipboard.writeText(store.generatedToken.token)
    ElMessage.success('Token 已复制到剪贴板')
  } catch (e) {
    ElMessage.error('复制失败，请手动复制')
  }
}

onMounted(() => {
  if (isAdmin.value) {
    store.fetchTokens()
  }
})
</script>

<style scoped>
.users-page {
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

.access-denied {
  margin-top: 64px;
}
</style>
