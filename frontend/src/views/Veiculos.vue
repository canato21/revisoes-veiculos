<template>
  <div class="fade-in">

    <div class="page-header">
      <h1>Veículos</h1>
      <p>Gerenciamento geral e edição de veículos cadastrados</p>
    </div>

    <div class="table-container">
      <div class="table-header">
        <div>
          <h3>{{ totalVeiculos }} veículos cadastrados</h3>
        </div>
        <div style="display:flex; gap:10px; align-items:center;">
          <input v-model="busca" placeholder="Buscar por marca, modelo, placa..."
            style="width:280px; padding:8px 12px; border:1.5px solid var(--gray-200); border-radius:var(--radius); font-size:13px; outline:none;"
            @focus="$event.target.style.borderColor = 'var(--primary)'"
            @blur="$event.target.style.borderColor = 'var(--gray-200)'" />
        </div>
      </div>

      <div v-if="carregando" class="loading">Carregando...</div>

      <table v-else>
        <thead>
          <tr>
            <th style="min-width:140px;">Proprietário</th>
            <th>Marca</th>
            <th>Modelo</th>
            <th>Ano</th>
            <th>Placa</th>
            <th>Cor</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="v in veiculos" :key="v.id" class="fade-in">
            <td style="max-width:160px;">
              <strong class="texto-truncado">{{ v.proprietario_nome }}</strong>
            </td>
            <td>{{ v.marca }}</td>
            <td>{{ v.modelo }}</td>
            <td>{{ v.ano }}</td>
            <td><span class="badge badge-success">{{ v.placa }}</span></td>
            <td>
              <div style="display:flex; align-items:center; gap:6px;">
                <span :style="{ backgroundColor: v.cor }"
                  style="width:12px; height:12px; border-radius:50%; display:inline-block; border:1px solid #ccc;"></span>
                {{ nomeDaCor(v.cor) }}
              </div>
            </td>
            <td>
              <div style="display:flex; gap:6px; align-items:center;">
                <button class="btn-icone" title="Editar Placa/Cor" @click="abrirModal(v)">✏️</button>
                <button class="btn-icone btn-icone-perigo" title="Excluir" @click="confirmarExclusao(v)">🗑️</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- ── PAGINAÇÃO ─────────────────────────────────────────────────────── -->
      <div
        style="display:flex; justify-content:space-between; align-items:center; padding:14px 24px; border-top:1px solid var(--gray-100);">
        <span v-if="totalVeiculos > 0" style="font-size:13px; color:var(--gray-500);">
          Mostrando {{ inicioPaginacao }} a {{ fimPaginacao }} de {{ totalVeiculos }} veículos
        </span>
        <span v-else style="font-size:13px; color:var(--gray-500);">
          Nenhum veículo encontrado
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


  <!-- ── MODAL CONFIRMAÇÃO EXCLUSÃO ────────────────────────────────────────── -->
  <div class="modal-overlay" v-if="modalExclusaoAberto" @click.self="modalExclusaoAberto = false">
    <div class="modal" style="max-width:420px;">
      <div style="text-align:center; padding:8px 0 20px;">
        <div style="font-size:48px; margin-bottom:12px;">⚠️</div>
        <h3 style="margin-bottom:8px;">Confirmar exclusão</h3>
        <p style="color:var(--gray-500); font-size:14px;">
          Deseja excluir o veículo
          <strong>{{ veiculoParaExcluir?.marca }} {{ veiculoParaExcluir?.modelo }}</strong>
          — placa <strong>{{ veiculoParaExcluir?.placa }}</strong>?
          Todas as revisões associadas também serão removidas.
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


  <!-- ── MODAL EDITAR VEÍCULO ──────────────────────────────────────────────── -->
  <div class="modal-overlay" v-if="modalAberto" @click.self="fecharModal">
    <div class="modal">
      <div class="modal-header">
        <h3>Editar Veículo de: {{ form.proprietario_nome }}</h3>
        <button class="modal-close" @click="fecharModal">×</button>
      </div>

      <div class="modal-body">
        <div class="form-grid">
          <div class="form-group">
            <label>Marca</label>
            <input :value="form.marca" readonly
              style="background:var(--gray-100); color:var(--gray-500); cursor:not-allowed;" />
          </div>
          <div class="form-group">
            <label>Modelo</label>
            <input :value="form.modelo" readonly
              style="background:var(--gray-100); color:var(--gray-500); cursor:not-allowed;" />
          </div>
          <div class="form-group">
            <label>Ano</label>
            <input :value="form.ano" readonly
              style="background:var(--gray-100); color:var(--gray-500); cursor:not-allowed;" />
          </div>

          <div class="form-group">
            <label>Placa</label>
            <input v-model="form.placa" placeholder="Ex: ABC1D23" :class="{ 'input-erro': erros.placa }"
              @input="form.placa = form.placa.toUpperCase(); delete erros.placa" maxlength="8" />
            <span class="msg-erro" v-if="erros.placa">{{ erros.placa }}</span>
          </div>

          <!-- Cor — bolinhas predefinidas + cor personalizada via color picker -->
          <div class="form-group full">
            <label>Cor</label>
            <div
              style="display:flex; flex-wrap:wrap; gap:9px; padding:14px; background:#fff; border:1.5px solid var(--gray-200); border-radius:8px;">

              <button v-for="c in todasAsCores" :key="c.valor" type="button" :title="c.nome"
                @click="selecionarCorVeiculo(c.valor)" :style="{
                  width: '30px', height: '30px', borderRadius: '50%',
                  background: c.valor,
                  border: form.cor === c.valor ? '3px solid var(--primary)' : '2px solid #d1d5db',
                  cursor: 'pointer', flexShrink: 0, outline: 'none',
                  boxShadow: c.valor === '#FFFFFF' ? 'inset 0 0 0 1px #e5e7eb' : '0 1px 3px rgba(0,0,0,.15)',
                  transform: form.cor === c.valor ? 'scale(1.15)' : 'scale(1)',
                  transition: 'transform .12s, border .12s'
                }">
              </button>

              <label title="Cor personalizada" style="width:30px; height:30px; border-radius:50%; border:2px dashed #9ca3af; cursor:pointer;
                       display:flex; align-items:center; justify-content:center; font-size:16px; font-weight:600;
                       flex-shrink:0; background:#fff; color:#9ca3af; position:relative; user-select:none;
                       transition:border-color .12s;" @mouseenter="$event.target.style.borderColor = 'var(--primary)'"
                @mouseleave="$event.target.style.borderColor = '#9ca3af'">
                +
                <input type="color" v-model="corCustomTemp" style="opacity:0; width:0; height:0; position:absolute;"
                  @change="abrirNomeCorCustom" />
              </label>
            </div>

            <div
              style="display:flex; align-items:center; gap:8px; padding:8px 12px; margin-top:8px; background:#fff; border:1px solid var(--gray-100); border-radius:8px;">
              <span
                :style="{ background: form.cor || '#e5e7eb', border: form.cor === '#FFFFFF' ? '1px solid #d1d5db' : 'none' }"
                style="width:18px; height:18px; border-radius:50%; flex-shrink:0; box-shadow:0 1px 3px rgba(0,0,0,.15);"></span>
              <span style="font-size:13px; color:var(--gray-700); font-weight:500;">
                {{ nomeDaCor(form.cor) || 'Nenhuma cor selecionada' }}
              </span>
            </div>

            <div v-if="nomeandoCorCustom"
              style="background:#fff; border:1.5px solid var(--primary); border-radius:10px; padding:16px; margin-top:12px;">
              <p style="font-size:13px; color:var(--gray-700); font-weight:600; margin:0 0 4px;">Nomear cor
                personalizada</p>
              <p style="font-size:12px; color:var(--gray-400); margin:0 0 12px; line-height:1.5;">
                Esta cor ficará salva como sugestão para os próximos cadastros.
              </p>
              <div style="display:flex; gap:8px; align-items:center; margin-bottom:12px;">
                <span :style="{ background: corCustomTemp }"
                  style="width:22px; height:22px; border-radius:50%; border:1px solid rgba(0,0,0,.12); flex-shrink:0; box-shadow:0 1px 3px rgba(0,0,0,.15);"></span>
                <input v-model="nomeCorCustom" placeholder="Ex: Azul Petróleo" maxlength="30"
                  style="flex:1; padding:8px 12px; border:1.5px solid var(--gray-200); border-radius:7px; font-size:13px; outline:none;"
                  @keyup.enter="confirmarCorCustom" @focus="$event.target.style.borderColor = 'var(--primary)'"
                  @blur="$event.target.style.borderColor = 'var(--gray-200)'" />
              </div>
              <div style="display:flex; gap:8px; justify-content:flex-end;">
                <button class="btn btn-ghost btn-sm" @click="cancelarCorCustom">Cancelar</button>
                <button class="btn btn-primary btn-sm" @click="confirmarCorCustom"
                  :disabled="!nomeCorCustom.trim()">Salvar cor</button>
              </div>
            </div>

            <span class="msg-erro" v-if="erros.cor">{{ erros.cor }}</span>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-ghost" @click="fecharModal">Cancelar</button>
        <button class="btn btn-primary" @click="salvar" :disabled="salvando">
          {{ salvando ? 'Salvando...' : 'Salvar Alterações' }}
        </button>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { veiculosAPI, pessoasAPI, api } from '../services/api'


// ── ESTADO ────────────────────────────────────────────────────────────────────

const veiculos = ref([])
const carregando = ref(true)
const modalAberto = ref(false)
const salvando = ref(false)
const erros = ref({})
const busca = ref('')
const totalVeiculos = ref(0)
const proximaPagina = ref(null)
const paginaAnterior = ref(null)
const paginaAtual = ref(1)
const limitePaginacao = ref(10)

// ── PAGINAÇÃO ─────────────────────────────────────────────────────────────────

const inicioPaginacao = computed(() => {
  if (totalVeiculos.value === 0) return 0
  return (paginaAtual.value - 1) * limitePaginacao.value + 1
})
const fimPaginacao = computed(() =>
  Math.min(paginaAtual.value * limitePaginacao.value, totalVeiculos.value)
)

// ── CORES: PADRÃO E CUSTOMIZADAS ──────────────────────────────────────────────

const CORES_KEY = 'veiculo_cores_customizadas'

const coresPadrao = [
  { nome: 'Branco', valor: '#FFFFFF' },
  { nome: 'Preto', valor: '#1a1a1a' },
  { nome: 'Prata', valor: '#C0C0C0' },
  { nome: 'Cinza', valor: '#808080' },
  { nome: 'Vermelho', valor: '#CC0000' },
  { nome: 'Azul', valor: '#1a4fa0' },
  { nome: 'Azul Claro', valor: '#4fc3f7' },
  { nome: 'Verde', valor: '#2e7d32' },
  { nome: 'Amarelo', valor: '#f9a825' },
  { nome: 'Laranja', valor: '#e65100' },
  { nome: 'Marrom', valor: '#5d4037' },
  { nome: 'Bege', valor: '#d7b899' },
  { nome: 'Dourado', valor: '#c8a84b' },
  { nome: 'Rosa', valor: '#e91e8c' },
  { nome: 'Vinho', valor: '#7b1fa2' },
]

const coresCustomizadas = ref([])
const corCustomTemp = ref('#000000')
const nomeandoCorCustom = ref(false)
const nomeCorCustom = ref('')

function carregarCoresCustomizadas() {
  try {
    const s = localStorage.getItem(CORES_KEY)
    coresCustomizadas.value = s ? JSON.parse(s) : []
  } catch { coresCustomizadas.value = [] }
}

const todasAsCores = computed(() => [...coresPadrao, ...coresCustomizadas.value])

function nomeDaCor(valor) {
  if (!valor) return '—'
  const c = todasAsCores.value.find(x => x.valor.toLowerCase() === valor.toLowerCase())
  return c ? c.nome : valor
}

function selecionarCorVeiculo(valor) {
  form.value.cor = valor
  delete erros.value.cor
}

function abrirNomeCorCustom() {
  const jaExiste = todasAsCores.value.find(c => c.valor.toLowerCase() === corCustomTemp.value.toLowerCase())
  if (jaExiste) { selecionarCorVeiculo(jaExiste.valor); return }
  nomeCorCustom.value = ''
  nomeandoCorCustom.value = true
}

function confirmarCorCustom() {
  if (!nomeCorCustom.value.trim()) return
  const nova = { nome: nomeCorCustom.value.trim(), valor: corCustomTemp.value }
  coresCustomizadas.value.push(nova)
  localStorage.setItem(CORES_KEY, JSON.stringify(coresCustomizadas.value))
  selecionarCorVeiculo(nova.valor)
  nomeandoCorCustom.value = false
  nomeCorCustom.value = ''
}

function cancelarCorCustom() {
  nomeandoCorCustom.value = false
  nomeCorCustom.value = ''
}

// ── EXCLUSÃO ──────────────────────────────────────────────────────────────────

const modalExclusaoAberto = ref(false)
const veiculoParaExcluir = ref(null)
const excluindo = ref(false)

function confirmarExclusao(veiculo) {
  veiculoParaExcluir.value = veiculo
  modalExclusaoAberto.value = true
}

async function deletar() {
  excluindo.value = true
  await veiculosAPI.deletar(veiculoParaExcluir.value.id)
  modalExclusaoAberto.value = false
  veiculoParaExcluir.value = null
  excluindo.value = false
  await carregar()
}

// ── FORMULÁRIO DE EDIÇÃO ──────────────────────────────────────────────────────

const form = ref({})

function abrirModal(veiculo) {
  form.value = { ...veiculo }
  erros.value = {}
  nomeandoCorCustom.value = false // Garante que a caixinha de nome fecha ao abrir novo modal
  modalAberto.value = true
}

function fecharModal() {
  modalAberto.value = false
  form.value = {}
  erros.value = {}
  nomeandoCorCustom.value = false
}

// ── BUSCA COM DEBOUNCE ────────────────────────────────────────────────────────

let buscaTimeout = null
watch(busca, (termo) => {
  clearTimeout(buscaTimeout)
  buscaTimeout = setTimeout(() => carregar(null, termo), 400)
})

// ── VALIDAÇÃO ─────────────────────────────────────────────────────────────────

function validarForm() {
  erros.value = {}
  if (!form.value.placa)
    erros.value.placa = 'Placa é obrigatória'
  else if (!/^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$|^[A-Z]{3}-[0-9]{4}$/.test(form.value.placa.toUpperCase()))
    erros.value.placa = 'Placa inválida (ex: ABC1D23)'
  if (!form.value.cor || form.value.cor.length < 2)
    erros.value.cor = 'Selecione uma cor'
  return Object.keys(erros.value).length === 0
}

// ── CRUD E PAGINAÇÃO ──────────────────────────────────────────────────────────

async function carregar(url = null, search = '') {
  carregando.value = true
  try {
    const res = url ? await api.get(url) : await veiculosAPI.listar(search)
    veiculos.value = res.data.results || res.data
    totalVeiculos.value = res.data.count || res.data.length
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

    if (veiculos.value.length > 0 && url === null) {
      limitePaginacao.value = veiculos.value.length
    }
  } catch (e) { console.error('Erro ao carregar dados', e) }
  finally { carregando.value = false }
}

async function salvar() {
  if (!validarForm()) return
  salvando.value = true
  try {
    await veiculosAPI.atualizar(form.value.id, form.value)
    await carregar()
    fecharModal()
  } catch (e) {
    if (e.response?.data?.placa) erros.value.placa = e.response.data.placa[0]
  }
  salvando.value = false
}

onMounted(() => {
  carregarCoresCustomizadas() // Carrega as cores salvas no localStorage ao abrir a tela
  carregar()
})
</script>