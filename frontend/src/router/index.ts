import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/',
    redirect: { name: 'dashboard' }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/strategy',
    name: 'strategy',
    component: () => import('@/views/Strategy.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'user'] }
  },
  {
    path: '/logs',
    name: 'logs',
    component: () => import('@/views/Logs.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'user'] }
  },
  {
    path: '/users',
    name: 'users',
    component: () => import('@/views/Users.vue'),
    meta: { requiresAuth: true, roles: ['admin'] }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, _from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }
  if (to.meta.roles && Array.isArray(to.meta.roles) && !to.meta.roles.includes(auth.role || '')) {
    next({ name: 'dashboard' })
    return
  }
  next()
})

export default router
