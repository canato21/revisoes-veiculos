<template>
  <div class="fade-in">
    <div class="page-header">
      <h1>Painel Principal</h1>
      <p>Gerenciador de revisões veiculares</p>
    </div>

    <!-- Alertas -->
    <div v-if="vencidas.length > 0 || vencendo30.length > 0" class="alertas-grid">

      <div v-if="vencidas.length > 0" class="alerta alerta-perigo">
        <div class="alerta-header" style="cursor:pointer" @click="abrirAlertaModal('vencidas')">
          <div class="alerta-icone">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
            </svg>
          </div>
          <div>
            <strong>Revisões Vencidas</strong>
            <span class="alerta-badge alerta-badge-perigo">{{ vencidas.length }}</span>
          </div>
          <span style="margin-left:auto; font-size:12px; color:var(--danger);">Ver todas →</span>
        </div>
        <div class="alerta-lista">
          <div v-for="v in vencidas.slice(0, 5)" :key="v.placa" class="alerta-item">
            <div class="alerta-item-info">
              <span class="alerta-placa">{{ v.placa }}</span>
              <span class="alerta-nome">{{ v.nome }}</span>
              <span class="alerta-veiculo">{{ v.marca }} {{ v.modelo }}</span>
            </div>
            <div class="alerta-data alerta-data-perigo">
              Venceu em {{ formatarData(v.proxima_revisao) }}
            </div>
          </div>
          <div v-if="vencidas.length > 5" class="alerta-mais" style="cursor:pointer"
            @click="abrirAlertaModal('vencidas')">
            +{{ vencidas.length - 5 }} mais veículos vencidos — clique para ver todos
          </div>
        </div>
      </div>

      <div v-if="vencendo30.length > 0" class="alerta alerta-aviso">
        <div class="alerta-header" style="cursor:pointer" @click="abrirAlertaModal('proximas')">
          <div class="alerta-icone">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <strong>Vencem em 30 dias</strong>
            <span class="alerta-badge alerta-badge-aviso">{{ vencendo30.length }}</span>
          </div>
          <span style="margin-left:auto; font-size:12px; color:var(--warning);">Ver todas →</span>
        </div>
        <div class="alerta-lista">
          <div v-for="v in vencendo30.slice(0, 5)" :key="v.placa" class="alerta-item">
            <div class="alerta-item-info">
              <span class="alerta-placa">{{ v.placa }}</span>
              <span class="alerta-nome">{{ v.nome }}</span>
              <span class="alerta-veiculo">{{ v.marca }} {{ v.modelo }}</span>
            </div>
            <div class="alerta-data alerta-data-aviso">
              {{ formatarData(v.proxima_revisao) }}
            </div>
          </div>
          <div v-if="vencendo30.length > 5" class="alerta-mais" style="cursor:pointer"
            @click="abrirAlertaModal('proximas')">
            +{{ vencendo30.length - 5 }} mais veículos — clique para ver todos
          </div>
        </div>
      </div>

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
        <div v-for="m in marcas.slice(0, 5)" :key="m.marca"
          style="display:flex; justify-content:space-between; padding:7px 0; border-bottom:1px solid #f5f5f5; font-size:14px;">
          <span>{{ m.marca }}</span>
          <span style="font-weight:700; color:#4fc3f7;">{{ m.total }}</span>
        </div>
      </div>
      <div class="card">
        <h3 style="margin-bottom:14px; font-size:15px;">🔧 Oficinas mais usadas</h3>
        <div v-if="oficinas.length === 0" class="loading">Carregando...</div>
        <div v-for="o in oficinas.slice(0, 5)" :key="o.oficina"
          style="display:flex; justify-content:space-between; padding:7px 0; border-bottom:1px solid #f5f5f5; font-size:14px;">
          <span style="font-size:13px;">{{ o.oficina }}</span>
          <span style="font-weight:700; color:#4caf50;">{{ o.total }}</span>
        </div>
      </div>
    </div>
  </div>

  <!-- ── MODAL DE ALERTAS (lista de veículos) ──────────────────────────────── -->
  <div class="modal-overlay" v-if="modalAlertasAberto" @click.self="modalAlertasAberto = false">
    <div class="modal modal-lg">
      <div class="modal-header">
        <div>
          <h3>{{ tipoAlerta === 'vencidas' ? 'Revisões Vencidas' : 'Revisões Próximas de Vencer' }}</h3>
          <p style="font-size:13px; color:var(--gray-400); margin-top:3px;">
            {{ tipoAlerta === 'vencidas' ? vencidas.length : vencendo30.length }} veículo(s)
          </p>
        </div>
        <button class="modal-close" @click="modalAlertasAberto = false">×</button>
      </div>
      <div class="modal-body">
        <table>
          <thead>
            <tr>
              <th>Placa</th>
              <th>Proprietário</th>
              <th>Veículo</th>
              <th>Última Revisão</th>
              <th>{{ tipoAlerta === 'vencidas' ? 'Venceu em' : 'Vence em' }}</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="v in (tipoAlerta === 'vencidas' ? vencidas : vencendo30)" :key="v.placa">
              <td><span class="badge badge-success">{{ v.placa }}</span></td>
              <td><strong>{{ v.nome }}</strong></td>
              <td>{{ v.marca }} {{ v.modelo }}</td>
              <td>{{ formatarData(v.ultima_revisao) }}</td>
              <td>
                <span class="badge" :class="tipoAlerta === 'vencidas' ? 'badge-vencida' : 'badge-proxima'">
                  {{ formatarData(v.proxima_revisao) }}
                </span>
              </td>
              <td>
                <button class="btn btn-primary btn-sm" @click="abrirNovaRevisao(v)">
                  + Registrar Revisão
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="modal-footer">
        <button class="btn btn-ghost" @click="modalAlertasAberto = false">Fechar</button>
      </div>
    </div>
  </div>

  <!-- ── MODAL DE REVISÃO — usa o componente padrão                         ── -->
  <!-- iniciarNovo=true  → abre direto no formulário                           -->
  <!-- semHistorico=true → "← Voltar" fecha o modal em vez de ir para a lista  -->
  <ModalRevisao v-if="veiculoParaRevisao" :veiculo="veiculoParaRevisao" :iniciar-novo="true" :sem-historico="true"
    @fechar="fecharRevisao" />

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { pessoasAPI, veiculosAPI, revisoesAPI } from '../services/api'
import ModalRevisao from '../components/ModalRevisao.vue'

// ── ESTADO ────────────────────────────────────────────────────────────────────

const totais = ref({ pessoas: 0, veiculos: 0, revisoes: 0, proximas: 0 })
const marcas = ref([])
const oficinas = ref([])
const proximas = ref([])
const vencidas = ref([])
const vencendo30 = ref([])

const modalAlertasAberto = ref(false)
const tipoAlerta = ref('')
const veiculoParaRevisao = ref(null)


// ── FUNÇÕES ───────────────────────────────────────────────────────────────────

function abrirAlertaModal(tipo) {
  tipoAlerta.value = tipo
  modalAlertasAberto.value = true
}

function abrirNovaRevisao(item) {
  veiculoParaRevisao.value = {
    id: item.veiculo_id,
    marca: item.marca,
    modelo: item.modelo,
    placa: item.placa
  }
  modalAlertasAberto.value = false
}

async function fecharRevisao() {
  veiculoParaRevisao.value = null
  // Recarrega os alertas para refletir a revisão salva
  try {
    const prox = await revisoesAPI.proximasRevisoes()
    const lista = Array.isArray(prox.data) ? prox.data : (prox.data.results || [])
    proximas.value = lista
    totais.value.proximas = lista.length
    const hoje = new Date()
    vencidas.value = lista.filter(p => p.proxima_revisao && new Date(p.proxima_revisao) < hoje)
    vencendo30.value = lista.filter(p => {
      if (!p.proxima_revisao) return false
      const diff = (new Date(p.proxima_revisao) - hoje) / (1000 * 60 * 60 * 24)
      return diff >= 0 && diff <= 30
    })
  } catch (e) { console.error(e) }
}

function formatarData(data) {
  if (!data) return '-'
  const [y, m, d] = data.split('T')[0].split('-')
  return `${d}/${m}/${y}`
}


// ── CARREGAMENTO INICIAL ──────────────────────────────────────────────────────

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

    totais.value.pessoas = p.data.count || pessoasList.length
    totais.value.veiculos = veiculosList.length
    totais.value.revisoes = revisoesList.length
    marcas.value = Array.isArray(pm.data) ? pm.data : (pm.data.results || [])
    proximas.value = Array.isArray(prox.data) ? prox.data : (prox.data.results || [])
    totais.value.proximas = proximas.value.length

    const hoje = new Date()
    vencidas.value = proximas.value.filter(p =>
      p.proxima_revisao && new Date(p.proxima_revisao) < hoje
    )
    vencendo30.value = proximas.value.filter(p => {
      if (!p.proxima_revisao) return false
      const diff = (new Date(p.proxima_revisao) - hoje) / (1000 * 60 * 60 * 24)
      return diff >= 0 && diff <= 30
    })

    const offMap = {}
    revisoesList.forEach(r => { offMap[r.oficina] = (offMap[r.oficina] || 0) + 1 })
    oficinas.value = Object.entries(offMap)
      .map(([oficina, total]) => ({ oficina, total }))
      .sort((a, b) => b.total - a.total)

  } catch (e) {
    console.error(e)
  }
})
</script>