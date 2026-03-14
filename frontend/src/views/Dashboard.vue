<template>
  <div class="fade-in">
    <div class="page-header">
      <h1>Dashboard</h1>
      <p>Bem-vindo ao sistema de controle de revisões de veículos</p>
    </div>

    <div class="cards-grid">
      <div class="card">
        <div class="card-icon">👥</div>
        <div class="card-value">{{ totais.pessoas }}</div>
        <div class="card-label">Pessoas cadastradas</div>
      </div>
      <div class="card">
        <div class="card-icon">🚗</div>
        <div class="card-value">{{ totais.veiculos }}</div>
        <div class="card-label">Veículos cadastrados</div>
      </div>
      <div class="card">
        <div class="card-icon">🔧</div>
        <div class="card-value">{{ totais.revisoes }}</div>
        <div class="card-label">Revisões realizadas</div>
      </div>
      <div class="card">
        <div class="card-icon">📅</div>
        <div class="card-value">{{ totais.proximas }}</div>
        <div class="card-label">Próximas revisões</div>
      </div>
    </div>

    <div class="cards-grid">
      <div class="card">
        <h3 style="margin-bottom:14px; font-size:15px;">🏆 Marcas mais comuns</h3>
        <div v-if="marcas.length === 0" class="loading">Carregando...</div>
        <div v-for="m in marcas.slice(0,5)" :key="m.marca"
             style="display:flex; justify-content:space-between; padding:7px 0; border-bottom:1px solid #f5f5f5; font-size:14px;">
          <span>{{ m.marca }}</span>
          <span style="font-weight:700; color:#4fc3f7;">{{ m.total }}</span>
        </div>
      </div>

      <div class="card">
        <h3 style="margin-bottom:14px; font-size:15px;">🔧 Oficinas mais usadas</h3>
        <div v-if="oficinas.length === 0" class="loading">Carregando...</div>
        <div v-for="o in oficinas.slice(0,5)" :key="o.oficina"
             style="display:flex; justify-content:space-between; padding:7px 0; border-bottom:1px solid #f5f5f5; font-size:14px;">
          <span style="font-size:13px;">{{ o.oficina }}</span>
          <span style="font-weight:700; color:#4caf50;">{{ o.total }}</span>
        </div>
      </div>

      <div class="card">
        <h3 style="margin-bottom:14px; font-size:15px;">📅 Próximas revisões</h3>
        <div v-if="proximas.length === 0" class="loading">Carregando...</div>
        <div v-for="p in proximas.slice(0,5)" :key="p.placa"
             style="padding:7px 0; border-bottom:1px solid #f5f5f5; font-size:13px;">
          <div style="font-weight:600;">{{ p.nome }}</div>
          <div style="color:#888;">{{ p.marca }} {{ p.modelo }} · {{ p.placa }}</div>
          <div style="color:#ff7043; font-size:12px;">{{ formatarData(p.proxima_revisao) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { pessoasAPI, veiculosAPI, revisoesAPI } from '../services/api'

const totais  = ref({ pessoas: 0, veiculos: 0, revisoes: 0, proximas: 0 })
const marcas  = ref([])
const oficinas = ref([])
const proximas = ref([])

function formatarData(data) {
  if (!data) return '-'
  return new Date(data).toLocaleDateString('pt-BR')
}

onMounted(async () => {
  try {
    const [p, v, r, pm, prox] = await Promise.all([
      pessoasAPI.listar(),
      veiculosAPI.listar(),
      revisoesAPI.listar(),
      veiculosAPI.porMarca(),
      revisoesAPI.proximasRevisoes(),
    ])

    const pessoasList = Array.isArray(p.data) ? p.data : (p.data.results || [])
    const veiculosList = Array.isArray(v.data) ? v.data : (v.data.results || [])
    const revisoesList = Array.isArray(r.data) ? r.data : (r.data.results || [])

    totais.value.pessoas  = pessoasList.length
    totais.value.veiculos = veiculosList.length
    totais.value.revisoes = revisoesList.length
    marcas.value = Array.isArray(pm.data) ? pm.data : (pm.data.results || [])
    proximas.value = Array.isArray(prox.data) ? prox.data : (prox.data.results || [])
    totais.value.proximas = proximas.value.length

    const offMap = {}
    revisoesList.forEach(r => {
      offMap[r.oficina] = (offMap[r.oficina] || 0) + 1
    })
    oficinas.value = Object.entries(offMap)
      .map(([oficina, total]) => ({ oficina, total }))
      .sort((a, b) => b.total - a.total)

  } catch (e) {
    console.error(e)
  }
})
</script>