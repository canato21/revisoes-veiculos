<template>
  <div class="fade-in">
    <div class="page-header">
      <h1>📊 Relatórios</h1>
      <p>Análises e gráficos do sistema</p>
    </div>

    <!-- Veículos por marca -->
    <div class="cards-grid" style="grid-template-columns: 1fr 1fr;">
      <div class="card">
        <h3 style="margin-bottom:16px;">🚗 Veículos por Marca</h3>
        <Bar v-if="marcasData" :data="marcasData" :options="opcoesBar" />
        <div v-else class="loading">Carregando...</div>
      </div>

      <div class="card">
        <h3 style="margin-bottom:16px;">👥 Veículos por Sexo</h3>
        <Pie v-if="sexoData" :data="sexoData" :options="opcoesPie" />
        <div v-else class="loading">Carregando...</div>
      </div>

      <div class="card">
        <h3 style="margin-bottom:16px;">🔧 Marcas com Mais Revisões</h3>
        <Bar v-if="revisoesMarcaData" :data="revisoesMarcaData" :options="opcoesBar" />
        <div v-else class="loading">Carregando...</div>
      </div>

      <div class="card">
        <h3 style="margin-bottom:16px;">🏆 Pessoas com Mais Revisões</h3>
        <Bar v-if="revisoesPessoaData" :data="revisoesPessoaData" :options="opcoesBar" />
        <div v-else class="loading">Carregando...</div>
      </div>
    </div>

    <!-- Próximas revisões -->
    <div class="table-container" style="margin-top:24px;">
      <div class="table-header">
        <h3>📅 Próximas Revisões Previstas</h3>
      </div>
      <div v-if="proximas.length === 0" class="loading">Carregando...</div>
      <table v-else>
        <thead>
          <tr>
            <th>Proprietário</th>
            <th>Veículo</th>
            <th>Placa</th>
            <th>Última Revisão</th>
            <th>Média (dias)</th>
            <th>Próxima Revisão</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in proximas" :key="p.placa" class="fade-in">
            <td><strong>{{ p.nome }}</strong></td>
            <td>{{ p.marca }} {{ p.modelo }}</td>
            <td><span class="badge badge-success">{{ p.placa }}</span></td>
            <td>{{ formatarData(p.ultima_revisao) }}</td>
            <td>{{ p.media_dias }} dias</td>
            <td>
              <span class="badge"
                :style="proximaStyle(p.proxima_revisao)">
                {{ formatarData(p.proxima_revisao) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Média de tempo entre revisões -->
    <div class="card" style="margin-top:24px;">
      <h3 style="margin-bottom:16px;">⏱️ Média de Dias Entre Revisões por Pessoa</h3>
      <Bar v-if="mediaTempoData" :data="mediaTempoData" :options="opcoesBar" />
      <div v-else class="loading">Carregando...</div>
    </div>

    <!-- Relatório por período -->
    <div class="card" style="margin-top:24px;">
      <h3 style="margin-bottom:16px;">📆 Revisões por Período</h3>
      <div style="display:flex; gap:12px; align-items:flex-end; margin-bottom:16px; flex-wrap:wrap;">
        <div class="form-group">
          <label>Data início</label>
          <input v-model="periodo.inicio" type="date" />
        </div>
        <div class="form-group">
          <label>Data fim</label>
          <input v-model="periodo.fim" type="date" />
        </div>
        <button class="btn btn-primary" @click="buscarPeriodo">🔍 Buscar</button>
      </div>
      <div v-if="revisoesPeriodo.length === 0" style="color:#aaa; font-size:14px;">
        Nenhuma revisão no período selecionado.
      </div>
      <table v-else>
        <thead>
          <tr>
            <th>Proprietário</th>
            <th>Veículo</th>
            <th>Data</th>
            <th>KM</th>
            <th>Valor</th>
            <th>Oficina</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in revisoesPeriodo" :key="r.id">
            <td>{{ r.proprietario_nome }}</td>
            <td>{{ r.veiculo_modelo }} ({{ r.veiculo_placa }})</td>
            <td>{{ formatarData(r.data_revisao) }}</td>
            <td>{{ r.kilometragem?.toLocaleString('pt-BR') }} km</td>
            <td>{{ formatarValor(r.valor) }}</td>
            <td>{{ r.oficina }}</td>
          </tr>
        </tbody>
      </table>
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
import { veiculosAPI, revisoesAPI } from '../services/api'

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend)

const marcasData        = ref(null)
const sexoData          = ref(null)
const revisoesMarcaData = ref(null)
const revisoesPessoaData= ref(null)
const mediaTempoData    = ref(null)
const proximas          = ref([])
const revisoesPeriodo   = ref([])
const periodo = ref({ inicio: '', fim: '' })

const CORES = [
  '#4fc3f7','#81c784','#ffb74d','#e57373','#ba68c8',
  '#4db6ac','#fff176','#f06292','#64b5f6','#a1887f'
]

const opcoesBar = {
  responsive: true,
  plugins: { legend: { display: false } },
  scales: { y: { beginAtZero: true } }
}
const opcoesPie = {
  responsive: true,
  plugins: { legend: { position: 'bottom' } }
}

function formatarData(data) {
  if (!data) return '-'
  return new Date(data).toLocaleDateString('pt-BR')
}

function formatarValor(valor) {
  return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function proximaStyle(data) {
  if (!data) return {}
  const diff = (new Date(data) - new Date()) / (1000 * 60 * 60 * 24)
  if (diff < 0)  return { background: '#ffebee', color: '#c62828' }
  if (diff < 30) return { background: '#fff3e0', color: '#e65100' }
  return { background: '#e8f5e9', color: '#2e7d32' }
}

async function buscarPeriodo() {
  if (!periodo.value.inicio || !periodo.value.fim) {
    alert('Selecione as datas!')
    return
  }
  const res = await revisoesAPI.porPeriodo(periodo.value.inicio, periodo.value.fim)
  revisoesPeriodo.value = res.data.results || res.data
}

onMounted(async () => {
  try {
    const [marcas, sexo, revMarcas, revPessoas, mediaTempo, prox] = await Promise.all([
      veiculosAPI.porMarca(),
      veiculosAPI.quemTemMais(),
      revisoesAPI.marcasMaisRevisoes(),
      revisoesAPI.pessoasMaisRevisoes(),
      revisoesAPI.mediaTempo(),
      revisoesAPI.proximasRevisoes(),
    ])

    // Gráfico marcas
    marcasData.value = {
      labels: marcas.data.map(m => m.marca),
      datasets: [{ data: marcas.data.map(m => m.total),
        backgroundColor: CORES, borderRadius: 6 }]
    }

    // Gráfico sexo
    sexoData.value = {
      labels: sexo.data.map(s => s.sexo === 'M' ? 'Masculino' : 'Feminino'),
      datasets: [{ data: sexo.data.map(s => s.total_veiculos),
        backgroundColor: ['#4fc3f7', '#f48fb1'], borderWidth: 0 }]
    }

    // Gráfico revisões por marca
    const rm = revMarcas.data.slice(0, 8)
    revisoesMarcaData.value = {
      labels: rm.map(r => r.veiculo__marca),
      datasets: [{ data: rm.map(r => r.total),
        backgroundColor: CORES, borderRadius: 6 }]
    }

    // Gráfico revisões por pessoa
    const rp = revPessoas.data.slice(0, 8)
    revisoesPessoaData.value = {
      labels: rp.map(r => r.veiculo__proprietario__nome?.split(' ')[0]),
      datasets: [{ data: rp.map(r => r.total),
        backgroundColor: CORES, borderRadius: 6 }]
    }

    // Gráfico média de tempo
    const mt = mediaTempo.data.slice(0, 8)
    mediaTempoData.value = {
      labels: mt.map(r => r.nome?.split(' ')[0]),
      datasets: [{ label: 'Dias', data: mt.map(r => Math.round(r.media_dias)),
        backgroundColor: '#4fc3f7', borderRadius: 6 }]
    }

    proximas.value = prox.data

  } catch (e) {
    console.error(e)
  }
})
</script>