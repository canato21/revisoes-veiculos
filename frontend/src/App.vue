<!--
  Este é o componente raiz da aplicação — o "esqueleto" que envolve todas as telas.
  Ele contém:
    - A barra de navegação superior (topbar)
    - O <RouterView> que renderiza a tela atual

  Quando o usuário navega para /pessoas, o RouterView troca automaticamente
  para o componente Pessoas.vue, sem recarregar a página.
-->

<template>
  <!-- .layout: div raiz que organiza topbar + conteúdo em coluna -->
  <div class="layout">

    <!-- ── BARRA DE NAVEGAÇÃO SUPERIOR ─────────────────────────────────── -->
    <header class="topbar">

      <!-- Logo e nome do sistema -->
      <div class="topbar-brand">
        <div class="logo-icon">
          <!-- Ícone SVG de carro (inline — não precisa de arquivo externo) -->
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10l2 2m0 0h10m-10 0V6m10 10l2-2V9.5a2 2 0 00-.586-1.414l-3.5-3.5A2 2 0 0016.5 4H13" />
          </svg>
        </div>
        <span class="brand-name">AutoRevisão</span>
      </div>

      <!-- Links de navegação centralizados -->
      <nav class="topbar-nav">

        <!--
          RouterLink: componente do Vue Router que cria links de navegação.
          'to': rota de destino
          'active-class': classe CSS aplicada quando este link está ativo
          'exact': para o Dashboard, só ativa em '/' exatamente (não em '/pessoas')
        -->
        <RouterLink to="/" class="top-nav-item" active-class="active" exact>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          Dashboard
        </RouterLink>

        <RouterLink to="/pessoas" class="top-nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Pessoas
        </RouterLink>

        <RouterLink to="/veiculos" class="top-nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10l2 2m0 0h10m-10 0V6m10 10l2-2V9.5a2 2 0 00-.586-1.414l-3.5-3.5A2 2 0 0016.5 4H13" />
          </svg>
          Veículos
        </RouterLink>

        <RouterLink to="/revisoes" class="top-nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Revisões
        </RouterLink>

        <RouterLink to="/relatorios" class="top-nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          Relatórios
        </RouterLink>
      </nav>

      <!-- Lado direito: nome do usuário logado + botão de sair -->
      <div class="topbar-right">
        <!-- Exibe o nome do usuário logado (salvo no localStorage no login) -->
        <span style="font-size:13px; color:var(--gray-500);">{{ usuario }}</span>

        <!-- Botão de logout -->
        <button class="btn btn-ghost btn-sm" @click="sair">Sair</button>
      </div>
    </header>

    <!-- ── CONTEÚDO PRINCIPAL ───────────────────────────────────────────── -->
    <!--
      RouterView: "buraco" onde o Vue Router injeta o componente da rota atual.
      Quando o usuário acessa /pessoas, este elemento vira <Pessoas />
      Quando acessa /veiculos, vira <Veiculos />, e assim por diante.
    -->
    <main class="main-content">
      <RouterView />
    </main>

  </div>
</template>

<script setup>
/**
 * Composition API com <script setup>
 * A sintaxe 'setup' é a forma moderna do Vue 3.
 * Tudo declarado aqui fica disponível automaticamente no template.
 */

import { ref } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'

// useRouter(): acessa o router para navegar programaticamente
const router = useRouter()

// ref(): cria uma variável reativa
// localStorage.getItem('usuario'): recupera o nome salvo no login
// || '': fallback caso não exista nada salvo
const usuario = ref(localStorage.getItem('usuario') || '')

/**
 * Função de logout.
 * Remove os dados de autenticação do localStorage e redireciona para login.
 * O interceptor do Axios também faz isso automaticamente quando o token expira,
 * mas aqui é o logout manual pelo botão "Sair".
 */
function sair() {
  localStorage.removeItem('token')    // remove o access token JWT
  localStorage.removeItem('usuario')  // remove o nome do usuário
  router.push('/login')               // navega para a tela de login
}
</script>
