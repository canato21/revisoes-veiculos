
/*
    O Vue Router gerencia a navegação entre as diferentes "páginas" do sistema
 * sem recarregar o navegador. Isso é chamado de SPA (Single Page Application).
 *
 * Quando o usuário clica em um link, o Vue Router:
 *   1. Intercepta a navegação
 *   2. Verifica se o usuário tem permissão (guarda de rota)
 *   3. Troca o componente exibido na tela (sem recarregar a página)
 */

import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Pessoas from '../views/Pessoas.vue'
import Veiculos from '../views/Veiculos.vue'
import Revisoes from '../views/Revisoes.vue'
import Relatorios from '../views/Relatorios.vue'
import Login from '../views/Login.vue'

/**
 * Definição das rotas do sistema.
 * Cada objeto mapeia um 'path' (URL) a um 'component' (tela Vue).
 * 'meta': dados extras sobre a rota.
 * 'meta.publico: true': rota acessível sem estar logado.
 */
const routes = [
    {
        path: '/login', component: Login,
        meta: { publico: true }
    }, // única rota acessível sem autenticação
    { path: '/', component: Dashboard },
    { path: '/pessoas', component: Pessoas },
    { path: '/veiculos', component: Veiculos },
    { path: '/revisoes', component: Revisoes },
    { path: '/relatorios', component: Relatorios },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Proteção de rotas — redireciona para login se não autenticado
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    if (!to.meta.publico && !token) {
        next('/login')
    } else if (to.path === '/login' && token) {
        next('/')
    } else {
        next()
    }
})

export default router