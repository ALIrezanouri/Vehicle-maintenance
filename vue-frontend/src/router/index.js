import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Vehicles from '../views/Vehicles.vue'
import Services from '../views/Services.vue'
import History from '../views/History.vue'
import Emergency from '../views/Emergency.vue'
import Admin from '../views/Admin.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/vehicles',
    name: 'Vehicles',
    component: Vehicles
  },
  {
    path: '/services',
    name: 'Services',
    component: Services
  },
  {
    path: '/history',
    name: 'History',
    component: History
  },
  {
    path: '/emergency',
    name: 'Emergency',
    component: Emergency
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router