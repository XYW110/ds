<template>
  <div class="login-page">
    <el-card class="login-card">
      <h2 class="title">DeepSeek 控制台登录</h2>
      <el-form :model="form" @submit.prevent="handleSubmit">
        <el-form-item label="访问 Token">
          <el-input v-model="form.token" placeholder="请输入访问 Token" />
        </el-form-item>
        <el-button type="primary" :loading="auth.loading" @click="handleSubmit" class="submit-btn">
          登录
        </el-button>
        <el-alert v-if="auth.error" type="error" :closable="false" show-icon class="error-msg" :title="auth.error" />
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const form = reactive({ token: '' })

const handleSubmit = async () => {
  if (!form.token) return
  try {
    await auth.login({ token: form.token })
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)
  } catch (error) {
    console.error('登录失败', error)
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1f2937, #111827);
}

.login-card {
  width: 360px;
}

.title {
  text-align: center;
  margin-bottom: 16px;
  color: #111827;
}

.submit-btn {
  width: 100%;
  margin-top: 12px;
}

.error-msg {
  margin-top: 12px;
}
</style>
