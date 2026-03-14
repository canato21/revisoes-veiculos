import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Pessoas from '../views/Pessoas.vue'
import Veiculos from '../views/Veiculos.vue'
import Revisoes from '../views/Revisoes.vue'
import Relatorios from '../views/Relatorios.vue'

const routes = [
    { path: '/', component: Dashboard },
    { path: '/pessoas', component: Pessoas },
    { path: '/veiculos', component: Veiculos },
    { path: '/revisoes', component: Revisoes },
    { path: '/relatorios', component: Relatorios },
]

export default createRouter({
    history: createWebHistory(),
    routes
})