<template>
  <div class="fade-in">
    <div class="page-header">
      <h1>Relatórios</h1>
      <p>Clique em qualquer gráfico para ver os detalhes</p>
    </div>

    <div class="relatorio-secao">
      <h2 class="relatorio-titulo">Veículos</h2>
      <div class="relatorio-cards-grid">

        <div class="relatorio-card" @click="abrirPopup('marcas')">
          <div class="card-header-row">
            <h3>Marcas por veículos</h3>
            <span class="toggle-hint">▼ detalhes</span>
          </div>
          <div class="grafico-compacto">
            <Bar v-if="marcasData" :data="marcasData" :options="opcoesBar" />
            <div v-else class="loading">Carregando...</div>
          </div>
        </div>

        <div class="relatorio-card" @click="abrirPopup('sexo')">
          <div class="card-header-row">
            <h3>Veículos por sexo</h3>
            <span class="toggle-hint">▼ detalhes</span>
          </div>
          <div class="grafico-compacto grafico-pie">
            <Pie v-if="sexoData" :data="sexoData" :options="opcoesPie" />
            <div v-else class="loading">Carregando...</div>
          </div>
        </div>

        <div class="relatorio-card relatorio-card-largo" @click="abrirPopup('marcasSexo')">
          <div class="card-header-row">
            <h3>Marcas por sexo</h3>
            <span class="toggle-hint">▼ detalhes</span>
          </div>
          <div class="grafico-compacto">
            <Bar v-if="marcasSexoData" :data="marcasSexoData" :options="opcoesBarEmpilhado" />
            <div v-else class="loading">Carregando...</div>
          </div>
        </div>

        <div class="relatorio-card relatorio-card-largo" @click="abrirPopup('veicPessoa')">
          <div class="card-header-row">
            <h3>Veículos por pessoa</h3>
            <span class="toggle-hint">▼ detalhes</span>
          </div>
          <div class="resumo-inline">
            <span class="resumo-stat">
              <strong>{{ veiculosPorPessoa.length }}</strong> proprietários
            </span>
            <span class="resumo-stat">
              <strong>{{veiculosPorPessoa.reduce((a, i) => a + i.veiculos.length, 0)}}</strong> veículos cadastrados
            </span>
          </div>
        </div>

      </div>
    </div>

    <div class="relatorio-secao">
      <h2 class="relatorio-titulo">Pessoas</h2>
      <div class="relatorio-cards-grid">

        <div class="relatorio-card" @click="abrirPopup('idadeMedia')">
          <div class="card-header-row">
            <h3>Pessoas por sexo e idade média</h3>
            <span class="toggle-hint">▼ detalhes</span>
          </div>
          <div class="grafico-compacto">
            <Bar v-if="idadeMediaData" :data="idadeMediaData" :options="opcoesBar" />
            <div v-else class="loading">Carregando...</div>
          </div>
        </div>

      </div>
    </div>

    <div class="relatorio-secao">
      <h2 class="relatorio-titulo">Revisões</h2>
      <div class="relatorio-cards-grid">

        <div class="relatorio-card" @click="abrirPopup('revMarcas')">
          <div class="card-header-row">
            <h3>Revisões por marca</h3>
            <span class="toggle-hint">▼ detalhes</span>
          </div>
          <div class="grafico-compacto">
            <Bar v-if="revisoesMarcaData" :data="revisoesMarcaData" :options="opcoesBar" />
            <div v-else class="loading">Carregando...</div>
          </div>
        </div>

        <div class="relatorio-card" @click="abrirPopup('revPessoas')">
          <div class="card-header-row">
            <h3>Revisões por pessoa</h3>
            <span class="toggle-hint">▼ detalhes</span>
          </div>
          <div class="grafico-compacto">
            <Bar v-if="revisoesPessoaData" :data="revisoesPessoaData" :options="opcoesBar" />
            <div v-else class="loading">Carregando...</div>
          </div>
        </div>

        <div class="relatorio-card" @click="abrirPopup('mediaTempo')">
          <div class="card-header-row">
            <h3>Média de dias entre revisões</h3>
            <span class="toggle-hint">▼ detalhes</span>
          </div>
          <div class="grafico-compacto">
            <Bar v-if="mediaTempoData" :data="mediaTempoData" :options="opcoesBar" />
            <div v-else class="loading">Carregando...</div>
          </div>
        </div>

        <div class="relatorio-card" @click="abrirPopup('oficinas')">
          <div class="card-header-row">
            <h3>Revisões por oficina</h3>
            <span class="toggle-hint">▼ detalhes</span>
          </div>
          <div class="grafico-compacto">
            <Bar v-if="oficinasData" :data="oficinasData" :options="opcoesBar" />
            <div v-else class="loading">Carregando...</div>
          </div>
        </div>

        <div class="relatorio-card relatorio-card-largo" @click="abrirPopup('proximas')">
          <div class="card-header-row">
            <h3>Próximas revisões previstas</h3>
            <span class="toggle-hint">▼ detalhes</span>
          </div>
          <div v-if="proximas.length === 0" class="loading">Carregando...</div>
          <div v-else style="display:flex; flex-direction:column; gap:6px; padding:4px 0;">
            <div v-for="p in proximas.slice(0, 8)" :key="p.placa"
              style="display:flex; align-items:center; gap:10px; font-size:13px;">
              <span class="badge badge-success" style="min-width:80px; text-align:center; font-size:11px;">{{ p.placa
              }}</span>
              <span style="min-width:130px; color:var(--gray-600);">{{ p.marca }} {{ p.modelo }}</span>
              <div style="flex:1; background:var(--gray-100); border-radius:20px; height:10px; overflow:hidden;">
                <div :style="{
                  width: barraStatus(p.proxima_revisao),
                  background: corBarra(p.proxima_revisao),
                  height: '100%',
                  borderRadius: '20px',
                  transition: 'width 0.4s'
                }"></div>
              </div>
              <span
                :style="{ color: corTexto(p.proxima_revisao), fontWeight: 600, minWidth: '140px', textAlign: 'right', fontSize: '12px' }">
                {{ statusRevisao(p.proxima_revisao) }}
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>

  <div class="modal-overlay" v-if="popupAberto" @click.self="fecharPopup">
    <div class="modal modal-lg">
      <div class="modal-header">
        <h3>{{ popupTitulo }}</h3>
        <button class="modal-close" @click="fecharPopup">×</button>
      </div>
      <div class="modal-body">

        <table v-if="popupAberto === 'marcas'">
          <thead>
            <tr>
              <th>Marca</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in marcas" :key="m.marca">
              <td><strong>{{ m.marca }}</strong></td>
              <td><span class="badge badge-success">{{ m.total }}</span></td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="popupAberto === 'sexo'">
          <thead>
            <tr>
              <th>Sexo</th>
              <th>Total de Veículos</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in sexoVeiculos" :key="s.sexo">
              <td><span class="badge" :class="s.sexo === 'M' ? 'badge-m' : 'badge-f'">{{ s.sexo === 'M' ? 'Masculino' :
                'Feminino' }}</span></td>
              <td><strong>{{ s.total_veiculos }}</strong></td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="popupAberto === 'marcasSexo'">
          <thead>
            <tr>
              <th>Marca</th>
              <th>Sexo</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in marcasPorSexo" :key="m.marca + m.proprietario__sexo">
              <td><strong>{{ m.marca }}</strong></td>
              <td><span class="badge" :class="m.proprietario__sexo === 'M' ? 'badge-m' : 'badge-f'">{{
                m.proprietario__sexo === 'M' ? 'Masculino' : 'Feminino' }}</span></td>
              <td>{{ m.total }}</td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="popupAberto === 'veicPessoa'">
          <thead>
            <tr>
              <th>Pessoa</th>
              <th>Sexo</th>
              <th>Veículos</th>
              <th>Quantidade</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in veiculosPorPessoa" :key="item.pessoa.id">
              <td><strong>{{ item.pessoa.nome }}</strong></td>
              <td><span class="badge" :class="item.pessoa.sexo === 'M' ? 'badge-m' : 'badge-f'">{{ item.pessoa.sexo ===
                'M' ? 'M' : 'F' }}</span></td>
              <td>
                <span v-for="v in item.veiculos" :key="v.id" class="badge badge-success" style="margin-right:4px;">{{
                  v.placa }}</span>
                <span v-if="item.veiculos.length === 0" style="color:var(--gray-400); font-size:12px;">—</span>
              </td>
              <td><strong>{{ item.veiculos.length }}</strong></td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="popupAberto === 'idadeMedia'">
          <thead>
            <tr>
              <th>Sexo</th>
              <th>Total</th>
              <th>Idade Média</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="badge badge-m">Masculino</span></td>
              <td>{{ pessoasPorSexo?.masculino?.length || 0 }}</td>
              <td><strong>{{ pessoasPorSexo?.idade_media_m }} anos</strong></td>
            </tr>
            <tr>
              <td><span class="badge badge-f">Feminino</span></td>
              <td>{{ pessoasPorSexo?.feminino?.length || 0 }}</td>
              <td><strong>{{ pessoasPorSexo?.idade_media_f }} anos</strong></td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="popupAberto === 'revMarcas'">
          <thead>
            <tr>
              <th>#</th>
              <th>Marca</th>
              <th>Revisões</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(m, i) in revisoesPorMarca" :key="m.veiculo__marca">
              <td style="color:var(--gray-400)">{{ i + 1 }}</td>
              <td><strong>{{ m.veiculo__marca }}</strong></td>
              <td><span class="badge badge-success">{{ m.total }}</span></td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="popupAberto === 'revPessoas'">
          <thead>
            <tr>
              <th>#</th>
              <th>Pessoa</th>
              <th>Revisões</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(p, i) in revisoesPorPessoa" :key="p.veiculo__proprietario__nome">
              <td style="color:var(--gray-400)">{{ i + 1 }}</td>
              <td><strong>{{ p.veiculo__proprietario__nome }}</strong></td>
              <td><span class="badge badge-success">{{ p.total }}</span></td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="popupAberto === 'mediaTempo'">
          <thead>
            <tr>
              <th>Pessoa</th>
              <th>Média (dias)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in mediaTempo" :key="m.nome">
              <td><strong>{{ m.nome }}</strong></td>
              <td>{{ Math.round(m.media_dias) }} dias</td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="popupAberto === 'oficinas'">
          <thead>
            <tr>
              <th>#</th>
              <th>Oficina</th>
              <th>Revisões</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(o, i) in oficinasData.labels" :key="o">
              <td style="color:var(--gray-400)">{{ i + 1 }}</td>
              <td><strong>{{ o }}</strong></td>
              <td><span class="badge badge-success">{{ oficinasData.datasets[0].data[i] }}</span></td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="popupAberto === 'proximas'">
          <thead>
            <tr>
              <th>Proprietário</th>
              <th>Veículo</th>
              <th>Placa</th>
              <th>Última Revisão</th>
              <th>Média (dias)</th>
              <th>Próxima Revisão</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in proximas" :key="p.placa">
              <td><strong>{{ p.nome }}</strong></td>
              <td>{{ p.marca }} {{ p.modelo }}</td>
              <td><span class="badge badge-success">{{ p.placa }}</span></td>
              <td>{{ formatarData(p.ultima_revisao) }}</td>
              <td>{{ p.media_dias }} dias</td>
              <td>{{ formatarData(p.proxima_revisao) }}</td>
              <td>
                <span class="badge" :style="proximaStyle(p.proxima_revisao)">
                  {{ statusRevisao(p.proxima_revisao) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>

      </div>
      <div class="modal-footer">
        <button class="btn btn-ghost" @click="fecharPopup">Fechar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Bar, Pie } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale,
  BarElement, ArcElement, Title, Tooltip, Legend
} from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels'
import { veiculosAPI, revisoesAPI, pessoasAPI } from '../services/api'

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend, ChartDataLabels)

// ── POPUP — controla qual tabela está aberta ───────────────────────────────────
const popupAberto = ref(null)

const titulos = {
  marcas: 'Marcas por veículos',
  sexo: 'Veículos por sexo',
  marcasSexo: 'Marcas por sexo',
  veicPessoa: 'Veículos por pessoa',
  idadeMedia: 'Pessoas por sexo e idade média',
  revMarcas: 'Revisões por marca',
  revPessoas: 'Revisões por pessoa',
  mediaTempo: 'Média de dias entre revisões',
  oficinas: 'Revisões por oficina',
  proximas: 'Próximas revisões previstas',
}

const popupTitulo = ref('')

function abrirPopup(nome) {
  popupAberto.value = nome
  popupTitulo.value = titulos[nome] || nome
}

function fecharPopup() {
  popupAberto.value = null
}

// ── Dados brutos ───────────────────────────────────────────────────────────────
const marcas = ref([])
const sexoVeiculos = ref([])
const marcasPorSexo = ref([])
const veiculosPorPessoa = ref([])
const pessoasPorSexo = ref(null)
const revisoesPorMarca = ref([])
const revisoesPorPessoa = ref([])
const mediaTempo = ref([])
const proximas = ref([])

// ── Dados para Chart.js ────────────────────────────────────────────────────────
const marcasData = ref(null)
const sexoData = ref(null)
const marcasSexoData = ref(null)
const idadeMediaData = ref(null)
const revisoesMarcaData = ref(null)
const revisoesPessoaData = ref(null)
const mediaTempoData = ref(null)
const proximasData = ref(null)
const oficinasData = ref(null)

// ── Paleta de cores ────────────────────────────────────────────────────────────
const CORES = [
  '#2563eb', '#16a34a', '#d97706', '#dc2626', '#7c3aed',
  '#0891b2', '#db2777', '#65a30d', '#ea580c', '#6366f1'
]

// ── Plugin datalabels — configuração base para barras ─────────────────────────
const datalabelsBar = {
  anchor: 'end',
  align: 'end',
  offset: 2,
  font: { size: 11, weight: 'bold' },
  color: '#374151',
  formatter: (v) => v || ''
}

// ── Opções de gráficos ─────────────────────────────────────────────────────────

const opcoesBar = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: { display: false },
    datalabels: datalabelsBar
  },
  scales: {
    y: { beginAtZero: true, ticks: { font: { size: 11 } } },
    x: { ticks: { font: { size: 11 } } }
  },
  layout: { padding: { top: 20 } }
}

const opcoesBarEmpilhado = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top', labels: { font: { size: 11 } } },
    datalabels: { ...datalabelsBar, anchor: 'center', align: 'center', color: "#ffffff  " }
  },
  scales: {
    x: { stacked: true, ticks: { font: { size: 12 } } },
    y: { stacked: true, beginAtZero: true, ticks: { font: { size: 12 } } }
  },
  layout: { padding: { top: 10 } }
}

// Próximas revisões — mostra dias restantes (positivo) ou vencidos (negativo)
// Cores: vermelho = vencida, laranja = urgente (≤30 dias), verde = ok
const opcoesProximas = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: ctx => {
          const v = ctx.raw
          if (v < 0) return `Vencida há ${Math.abs(v)} dias`
          if (v === 0) return 'Vence hoje'
          return `Faltam ${v} dias`
        }
      }
    },
    datalabels: {
      anchor: 'end',
      align: ctx => ctx.raw < 0 ? 'start' : 'end',
      offset: 4,
      font: { size: 10, weight: 'bold' },
      color: '#374151',
      formatter: v => v < 0 ? `${v}d` : `+${v}d`
    }
  },
  scales: {
    y: {
      ticks: { font: { size: 11 }, callback: v => `${v}d` },
    },
    x: { ticks: { font: { size: 11 } } }
  },
  layout: { padding: { top: 20, bottom: 10 } }
}

const opcoesPie = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: { position: 'bottom', labels: { font: { size: 12 } } },
    datalabels: {
      color: '#fff',
      font: { size: 13, weight: 'bold' },
      formatter: (value, ctx) => {
        const total = ctx.dataset.data.reduce((a, b) => a + b, 0)
        const pct = total ? Math.round((value / total) * 100) : 0
        return `${value}\n(${pct}%)`
      }
    }
  }
}

// ── Helpers ────────────────────────────────────────────────────────────────────

function formatarData(data) {
  if (!data) return '-'
  const [y, m, d] = data.toString().split('T')[0].split('-')
  return `${d}/${m}/${y}`
}

function formatarValor(valor) {
  return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function diasParaRevisao(data) {
  if (!data) return null
  return Math.round((new Date(data) - new Date()) / (1000 * 60 * 60 * 24))
}

// Barra visual de status — largura proporcional aos dias restantes (0–100%)
// Vencida: 100% vermelho; Ok: proporcional ao tempo usado do intervalo
function barraStatus(data) {
  const diff = diasParaRevisao(data)
  if (diff === null) return '0%'
  if (diff <= 0) return '100%'  // vencida — barra cheia
  if (diff <= 30) return `${Math.round(70 + (30 - diff))}%`  // urgente: 70–100%
  if (diff <= 90) return `${Math.round(30 + ((90 - diff) / 90) * 40)}%`  // atenção
  return '20%'  // ok — barra curta
}

function corBarra(data) {
  const diff = diasParaRevisao(data)
  if (diff === null || diff <= 0) return '#dc2626'
  if (diff <= 30) return '#d97706'
  return '#16a34a'
}

function corTexto(data) {
  const diff = diasParaRevisao(data)
  if (diff === null || diff <= 0) return '#dc2626'
  if (diff <= 30) return '#d97706'
  return '#16a34a'
}

function proximaStyle(data) {
  const diff = diasParaRevisao(data)
  if (diff === null) return {}
  if (diff < 0) return { background: '#fee2e2', color: '#dc2626' }
  if (diff <= 30) return { background: '#fef3c7', color: '#d97706' }
  return { background: '#f0fdf4', color: '#16a34a' }
}

function statusRevisao(data) {
  const diff = diasParaRevisao(data)
  if (diff === null) return '—'
  if (diff < 0) return `Vencida há ${Math.abs(diff)} dias`
  if (diff === 0) return 'Vence hoje'
  if (diff <= 30) return `Faltam ${diff} dias`
  return `Faltam ${diff} dias`
}

// ── Carregamento ───────────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    const [
      resMarcas, resSexo, resMarcasSexo, resPorPessoa,
      resPorSexo, resRevMarcas, resRevPessoas,
      resMediaTempo, resProximas, resOficinas
    ] = await Promise.all([
      veiculosAPI.porMarca(),
      veiculosAPI.quemTemMais(),
      veiculosAPI.marcasPorSexo(),
      veiculosAPI.porPessoa(),
      pessoasAPI.porSexo(),
      revisoesAPI.marcasMaisRevisoes(),
      revisoesAPI.pessoasMaisRevisoes(),
      revisoesAPI.mediaTempo(),
      revisoesAPI.proximasRevisoes(),
      revisoesAPI.porOficina()
    ])

    // Marcas
    marcas.value = resMarcas.data
    marcasData.value = {
      labels: resMarcas.data.map(m => m.marca),
      datasets: [{ data: resMarcas.data.map(m => m.total), backgroundColor: CORES, borderRadius: 6 }]
    }

    // Sexo veículos
    sexoVeiculos.value = resSexo.data
    sexoData.value = {
      labels: resSexo.data.map(s => s.sexo === 'M' ? 'Masculino' : 'Feminino'),
      datasets: [{
        data: resSexo.data.map(s => s.total_veiculos),
        backgroundColor: ['#2563eb', '#db2777'],
        borderWidth: 0
      }]
    }

    // Marcas por sexo (empilhado)
    marcasPorSexo.value = resMarcasSexo.data
    const marcasUnicas = [...new Set(resMarcasSexo.data.map(m => m.marca))]
    marcasSexoData.value = {
      labels: marcasUnicas,
      datasets: [
        {
          label: 'Masculino',
          data: marcasUnicas.map(marca => {
            const item = resMarcasSexo.data.find(m => m.marca === marca && m.proprietario__sexo === 'M')
            return item ? item.total : 0
          }),
          backgroundColor: '#2563eb', borderRadius: 4
        },
        {
          label: 'Feminino',
          data: marcasUnicas.map(marca => {
            const item = resMarcasSexo.data.find(m => m.marca === marca && m.proprietario__sexo === 'F')
            return item ? item.total : 0
          }),
          backgroundColor: '#db2777', borderRadius: 4
        }
      ]
    }

    // Veículos por pessoa
    veiculosPorPessoa.value = resPorPessoa.data

    // Idade média por sexo
    pessoasPorSexo.value = resPorSexo.data
    idadeMediaData.value = {
      labels: ['Masculino', 'Feminino'],
      datasets: [{
        data: [resPorSexo.data.idade_media_m, resPorSexo.data.idade_media_f],
        backgroundColor: ['#2563eb', '#db2777'], borderRadius: 6
      }]
    }

    // Revisões por marca
    revisoesPorMarca.value = resRevMarcas.data
    const rm = resRevMarcas.data.slice(0, 8)
    revisoesMarcaData.value = {
      labels: rm.map(r => r.veiculo__marca),
      datasets: [{ data: rm.map(r => r.total), backgroundColor: CORES, borderRadius: 6 }]
    }

    // Revisões por pessoa
    revisoesPorPessoa.value = resRevPessoas.data
    const rp = resRevPessoas.data.slice(0, 8)
    revisoesPessoaData.value = {
      labels: rp.map(r => r.veiculo__proprietario__nome?.split(' ')[0]),
      datasets: [{ data: rp.map(r => r.total), backgroundColor: CORES, borderRadius: 6 }]
    }

    // Média de tempo
    mediaTempo.value = resMediaTempo.data
    const mt = resMediaTempo.data.slice(0, 8)
    mediaTempoData.value = {
      labels: mt.map(r => r.nome?.split(' ')[0]),
      datasets: [{ data: mt.map(r => Math.round(r.media_dias)), backgroundColor: '#2563eb', borderRadius: 6 }]
    }

    // Próximas revisões — mostra dias restantes com cor por urgência
    proximas.value = resProximas.data
    const hoje = new Date()
    const prox10 = resProximas.data.slice(0, 10)
    proximasData.value = {
      labels: prox10.map(p => p.placa),
      datasets: [{
        data: prox10.map(p => Math.round((new Date(p.proxima_revisao) - hoje) / (1000 * 60 * 60 * 24))),
        backgroundColor: prox10.map(p => {
          const diff = (new Date(p.proxima_revisao) - hoje) / (1000 * 60 * 60 * 24)
          if (diff < 0) return '#dc2626' // vencida
          if (diff <= 30) return '#d97706' // urgente
          return '#16a34a'                  // ok
        }),
        borderRadius: 6
      }]
    }

    // Revisões por oficina
    oficinasData.value = {
      labels: resOficinas.data.map(o => o.oficina),
      datasets: [{ data: resOficinas.data.map(o => o.total), backgroundColor: CORES, borderRadius: 6 }]
    }

  } catch (e) {
    console.error('Erro ao carregar relatórios:', e)
  }
})
</script>