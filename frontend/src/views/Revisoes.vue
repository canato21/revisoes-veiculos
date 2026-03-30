<template>
  <div class="fade-in">
    <div class="page-header">
      <h1>Revisões</h1>
      <p>Gerenciamento e histórico de todas as revisões</p>
    </div>

    <div class="table-container">
      <div class="table-header">
        <div>
          <h3>{{ totalRevisoes }} revisões no total</h3>
        </div>
        <div style="display:flex; gap:10px; align-items:center;">
          <input v-model="busca" placeholder="Buscar por placa, modelo, oficina..."
            style="width:280px; padding:8px 12px; border:1.5px solid var(--gray-200); border-radius:var(--radius); font-size:13px; outline:none;"
            @focus="$event.target.style.borderColor = 'var(--primary)'"
            @blur="$event.target.style.borderColor = 'var(--gray-200)'" />
        </div>
      </div>

      <div v-if="carregando" class="loading">Carregando...</div>

      <table v-else>
        <thead>
          <tr>
            <th>Proprietário</th>
            <th>Veículo</th>
            <th>Placa</th>
            <th>Data</th>
            <th>KM</th>
            <th>Oficina</th>
            <th>Valor</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in revisoes" :key="r.id" class="fade-in">
            <td style="max-width:140px;">
              <strong class="texto-truncado">{{ r.proprietario_nome }}</strong>
            </td>
            <td>{{ r.veiculo_modelo }}</td>
            <td><span class="badge badge-success">{{ r.veiculo_placa }}</span></td>
            <td>{{ formatarData(r.data_revisao) }}</td>
            <td>{{ Number(r.kilometragem).toLocaleString('pt-BR') }} km</td>
            <td style="max-width:120px;">
              <span class="texto-truncado">{{ r.oficina }}</span>
            </td>
            <td>{{ formatarValor(r.valor) }}</td>
            <td>
              <div style="display:flex; gap:6px; align-items:center;">
                <button class="btn-icone" title="Editar" @click="editarRevisao(r)">✏️</button>
                <button class="btn-icone btn-icone-perigo" title="Excluir" @click="confirmarExclusao(r)">🗑️</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- ── PAGINAÇÃO — igual ao Veiculos.vue e Pessoas.vue ──────────────── -->
      <div
        style="display:flex; justify-content:space-between; align-items:center; padding:14px 24px; border-top:1px solid var(--gray-100);">
        <span v-if="totalRevisoes > 0" style="font-size:13px; color:var(--gray-500);">
          Mostrando {{ inicioPaginacao }} a {{ fimPaginacao }} de {{ totalRevisoes }} revisões
        </span>
        <span v-else style="font-size:13px; color:var(--gray-500);">
          Nenhuma revisão encontrada
        </span>
        <div style="display:flex; gap:8px;">
          <button class="btn btn-ghost btn-sm" :disabled="!paginaAnterior" @click="carregar(paginaAnterior)">←
            Anterior</button>
          <button class="btn btn-ghost btn-sm" :disabled="!proximaPagina" @click="carregar(proximaPagina)">Próxima
            →</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ── MODAL CONFIRMAÇÃO DE EXCLUSÃO ────────────────────────────────────── -->
  <div class="modal-overlay" v-if="modalExclusaoAberto" @click.self="modalExclusaoAberto = false">
    <div class="modal" style="max-width:420px;">
      <div style="text-align:center; padding:8px 0 20px;">
        <div style="font-size:48px; margin-bottom:12px;">⚠️</div>
        <h3 style="margin-bottom:8px;">Confirmar exclusão</h3>
        <p style="color:var(--gray-500); font-size:14px;">
          Deseja excluir a revisão de
          <strong>{{ revisaoParaExcluir?.veiculo_modelo }}</strong>
          do dia <strong>{{ formatarData(revisaoParaExcluir?.data_revisao) }}</strong>?
          Esta ação não pode ser desfeita.
        </p>
      </div>
      <div style="display:flex; justify-content:center; gap:12px; padding:0 0 8px;">
        <button class="btn btn-ghost" @click="modalExclusaoAberto = false">Cancelar</button>
        <button class="btn btn-danger" @click="deletar" :disabled="excluindo">
          {{ excluindo ? 'Excluindo...' : 'Sim, excluir' }}
        </button>
      </div>
    </div>
  </div>

  <!-- ── MODAL DE REVISÃO — componente reutilizável ───────────────────────── -->
  <ModalRevisao v-if="modalAberto && veiculoSelecionado" :veiculo="veiculoSelecionado" @fechar="fecharModal" />

</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { revisoesAPI, api } from '../services/api'
import ModalRevisao from '../components/ModalRevisao.vue'

// ── ESTADO ────────────────────────────────────────────────────────────────────

const revisoes = ref([])
const carregando = ref(true)
const busca = ref('')
const totalRevisoes = ref(0)
const proximaPagina = ref(null)
const paginaAnterior = ref(null)
const paginaAtual = ref(1)
const limitePaginacao = ref(10)

// ── PAGINAÇÃO — igual ao Veiculos.vue ─────────────────────────────────────────

const inicioPaginacao = computed(() => {
  if (totalRevisoes.value === 0) return 0
  return (paginaAtual.value - 1) * limitePaginacao.value + 1
})
const fimPaginacao = computed(() =>
  Math.min(paginaAtual.value * limitePaginacao.value, totalRevisoes.value)
)

// ── EXCLUSÃO ──────────────────────────────────────────────────────────────────

const modalExclusaoAberto = ref(false)
const revisaoParaExcluir = ref(null)
const excluindo = ref(false)

function confirmarExclusao(r) {
  revisaoParaExcluir.value = r
  modalExclusaoAberto.value = true
}

async function deletar() {
  excluindo.value = true
  try {
    await revisoesAPI.deletar(revisaoParaExcluir.value.id)
    modalExclusaoAberto.value = false
    revisaoParaExcluir.value = null
    await carregar()
  } catch (e) { console.error(e) }
  excluindo.value = false
}

// ── MODAL DE EDIÇÃO — usa o ModalRevisao ──────────────────────────────────────

const modalAberto = ref(false)
const veiculoSelecionado = ref(null)

function editarRevisao(r) {
  // Monta o objeto que o ModalRevisao espera
  veiculoSelecionado.value = {
    id: r.veiculo,
    marca: r.veiculo_marca || '',
    modelo: r.veiculo_modelo || '',
    placa: r.veiculo_placa || ''
  }
  modalAberto.value = true
}

function fecharModal() {
  modalAberto.value = false
  veiculoSelecionado.value = null
  carregar()
}

// ── BUSCA COM DEBOUNCE ────────────────────────────────────────────────────────

let buscaTimeout = null
watch(busca, (termo) => {
  clearTimeout(buscaTimeout)
  buscaTimeout = setTimeout(() => carregar(null, termo), 400)
})

// ── FORMATADORES ──────────────────────────────────────────────────────────────

function formatarData(data) {
  if (!data) return '—'
  const [y, m, d] = data.split('-')
  return `${d}/${m}/${y}`
}

function formatarValor(valor) {
  return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

// ── CRUD E PAGINAÇÃO ──────────────────────────────────────────────────────────

async function carregar(url = null, search = '') {
  carregando.value = true
  try {
    const res = url ? await api.get(url) : await revisoesAPI.listar('', search)
    revisoes.value = res.data.results || res.data
    totalRevisoes.value = res.data.count || res.data.length
    proximaPagina.value = res.data.next || null
    paginaAnterior.value = res.data.previous || null

    if (url) {
      try {
        const p = new URL(url).searchParams.get('page')
        paginaAtual.value = p ? parseInt(p) : 1
      } catch { paginaAtual.value = 1 }
    } else {
      paginaAtual.value = 1
    }

    if (revisoes.value.length > 0 && url === null) {
      limitePaginacao.value = revisoes.value.length
    }
  } catch (e) { console.error('Erro ao carregar revisões', e) }
  finally { carregando.value = false }
}

onMounted(carregar)
</script>