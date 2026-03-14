<template>
  <div class="fade-in">
    <div class="page-header">
      <h1>🔧 Revisões</h1>
      <p>Cadastro e gerenciamento de revisões</p>
    </div>

    <div class="table-container">
      <div class="table-header">
        <h3>{{ revisoes.length }} revisões cadastradas</h3>
        <button class="btn btn-primary" @click="abrirModal()">+ Nova Revisão</button>
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
            <th>Valor</th>
            <th>Oficina</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in revisoes" :key="r.id" class="fade-in">
            <td><strong>{{ r.proprietario_nome }}</strong></td>
            <td>{{ r.veiculo_modelo }}</td>
            <td><span class="badge badge-success">{{ r.veiculo_placa }}</span></td>
            <td>{{ formatarData(r.data_revisao) }}</td>
            <td>{{ r.kilometragem.toLocaleString('pt-BR') }} km</td>
            <td>{{ formatarValor(r.valor) }}</td>
            <td>{{ r.oficina }}</td>
            <td>
              <button class="btn btn-warning btn-sm" @click="abrirModal(r)">✏️</button>
              <button class="btn btn-danger btn-sm" style="margin-left:6px" @click="deletar(r)">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div class="modal-overlay" v-if="modalAberto" @click.self="fecharModal">
      <div class="modal">
        <h3>{{ editando ? '✏️ Editar Revisão' : '➕ Nova Revisão' }}</h3>
        <div class="form-grid">
          <div class="form-group full">
            <label>Veículo</label>
            <select v-model="form.veiculo">
              <option value="">Selecione o veículo...</option>
              <option v-for="v in veiculos" :key="v.id" :value="v.id">
                {{ v.proprietario_nome }} — {{ v.marca }} {{ v.modelo }} ({{ v.placa }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Data da Revisão</label>
            <input v-model="form.data_revisao" type="date" />
          </div>
          <div class="form-group">
            <label>Kilometragem</label>
            <input v-model="form.kilometragem" type="number" placeholder="Ex: 45000" />
          </div>
          <div class="form-group">
            <label>Valor (R$)</label>
            <input v-model="form.valor" type="number" step="0.01" placeholder="Ex: 350.00" />
          </div>
          <div class="form-group">
            <label>Oficina</label>
            <input v-model="form.oficina" placeholder="Ex: Auto Center Silva" />
          </div>
          <div class="form-group full">
            <label>Descrição</label>
            <textarea v-model="form.descricao" placeholder="Ex: Troca de óleo e filtro..."></textarea>
          </div>
        </div>
        <div class="form-actions">
          <button class="btn btn-danger" @click="fecharModal">Cancelar</button>
          <button class="btn btn-success" @click="salvar">
            {{ salvando ? 'Salvando...' : '💾 Salvar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { revisoesAPI, veiculosAPI } from '../services/api'

const revisoes    = ref([])
const veiculos    = ref([])
const carregando  = ref(true)
const modalAberto = ref(false)
const editando    = ref(null)
const salvando    = ref(false)

const formVazio = () => ({
  veiculo: '', data_revisao: '', kilometragem: '',
  valor: '', oficina: '', descricao: ''
})
const form = ref(formVazio())

function formatarData(data) {
  if (!data) return '-'
  const [y, m, d] = data.split('-')
  return `${d}/${m}/${y}`
}

function formatarValor(valor) {
  return Number(valor).toLocaleString('pt-BR', {
    style: 'currency', currency: 'BRL'
  })
}

async function carregar() {
  carregando.value = true
  const [r, v] = await Promise.all([
    revisoesAPI.listar(),
    veiculosAPI.listar()
  ])
  revisoes.value = r.data.results || r.data
  veiculos.value = v.data.results || v.data
  carregando.value = false
}

function abrirModal(revisao = null) {
  editando.value = revisao
  form.value = revisao ? { ...revisao } : formVazio()
  modalAberto.value = true
}

function fecharModal() {
  modalAberto.value = false
  editando.value = null
  form.value = formVazio()
}

async function salvar() {
  if (!form.value.veiculo || !form.value.data_revisao || !form.value.kilometragem) {
    alert('Preencha todos os campos obrigatórios!')
    return
  }
  salvando.value = true
  try {
    if (editando.value) {
      await revisoesAPI.atualizar(editando.value.id, form.value)
    } else {
      await revisoesAPI.criar(form.value)
    }
    await carregar()
    fecharModal()
  } catch (e) {
    alert('Erro ao salvar: ' + (e.response?.data ? JSON.stringify(e.response.data) : e.message))
  }
  salvando.value = false
}

async function deletar(revisao) {
  if (!confirm(`Deseja excluir esta revisão?`)) return
  await revisoesAPI.deletar(revisao.id)
  await carregar()
}

onMounted(carregar)
</script>