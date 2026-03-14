<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <h2>🚗 Revisões</h2>
        <span>Sistema de Veículos</span>
      </div>
      <nav class="sidebar-nav">
        <RouterLink to="/" class="nav-item" active-class="active" exact>
          <span class="nav-icon">🏠</span>
          <span class="nav-label">Dashboard</span>
        </RouterLink>
        <RouterLink to="/pessoas" class="nav-item" active-class="active">
          <span class="nav-icon">👥</span>
          <span class="nav-label">Pessoas</span>
        </RouterLink>
        <RouterLink to="/veiculos" class="nav-item" active-class="active">
          <span class="nav-icon">🚗</span>
          <span class="nav-label">Veículos</span>
        </RouterLink>
        <RouterLink to="/revisoes" class="nav-item" active-class="active">
          <span class="nav-icon">🔧</span>
          <span class="nav-label">Revisões</span>
        </RouterLink>
        <RouterLink to="/relatorios" class="nav-item" active-class="active">
          <span class="nav-icon">📊</span>
          <span class="nav-label">Relatórios</span>
        </RouterLink>
      </nav>
    </aside>
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>