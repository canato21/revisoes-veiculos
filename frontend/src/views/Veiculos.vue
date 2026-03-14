<template>
  <div class="fade-in">
    <div class="page-header">
      <h1>🚗 Veículos</h1>
      <p>Cadastro e gerenciamento de veículos</p>
    </div>

    <div class="table-container">
      <div class="table-header">
        <h3>{{ veiculos.length }} veículos cadastrados</h3>
        <button class="btn btn-primary" @click="abrirModal()">+ Novo Veículo</button>
      </div>

      <div v-if="carregando" class="loading">Carregando...</div>

      <table v-else>
        <thead>
          <tr>
            <th>Proprietário</th>
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
            <td><strong>{{ v.proprietario_nome }}</strong></td>
            <td>{{ v.marca }}</td>
            <td>{{ v.modelo }}</td>
            <td>{{ v.ano }}</td>
            <td><span class="badge badge-success">{{ v.placa }}</span></td>
            <td>{{ v.cor }}</td>
            <td>
              <button class="btn btn-warning btn-sm" @click="abrirModal(v)">✏️ Editar</button>
              <button class="btn btn-danger btn-sm" style="margin-left:6px" @click="deletar(v)">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div class="modal-overlay" v-if="modalAberto" @click.self="fecharModal">
      <div class="modal">
        <h3>{{ editando ? '✏️ Editar Veículo' : '➕ Novo Veículo' }}</h3>
        <div class="form-grid">
          <div class="form-group full">
            <label>Proprietário</label>
            <select v-model="form.proprietario">
              <option value="">Selecione o proprietário...</option>
              <option v-for="p in pessoas" :key="p.id" :value="p.id">
                {{ p.nome }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Marca</label>
            <input v-model="form.marca" placeholder="Ex: Toyota" />
          </div>
          <div class="form-group">
            <label>Modelo</label>
            <input v-model="form.modelo" placeholder="Ex: Corolla" />
          </div>
          <div class="form-group">
            <label>Ano</label>
            <input v-model="form.ano" type="number" placeholder="Ex: 2022" />
          </div>
          <div class="form-group">
            <label>Placa</label>
            <input v-model="form.placa" placeholder="Ex: ABC1D23" />
          </div>
          <div class="form-group full">
            <label>Cor</label>
            <input v-model="form.cor" placeholder="Ex: Prata" />
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
import { veiculosAPI, pessoasAPI } from '../services/api'

const veiculos    = ref([])
const pessoas     = ref([])
const carregando  = ref(true)
const modalAberto = ref(false)
const editando    = ref(null)
const salvando    = ref(false)

const formVazio = () => ({
  proprietario: '', marca: '', modelo: '',
  ano: '', placa: '', cor: ''
})
const form = ref(formVazio())

async function carregar() {
  carregando.value = true
  const [v, p] = await Promise.all([
    veiculosAPI.listar(),
    pessoasAPI.listar()
  ])
  veiculos.value = v.data.results || v.data
  pessoas.value  = p.data.results || p.data
  carregando.value = false
}

function abrirModal(veiculo = null) {
  editando.value = veiculo
  form.value = veiculo ? { ...veiculo } : formVazio()
  modalAberto.value = true
}

function fecharModal() {
  modalAberto.value = false
  editando.value = null
  form.value = formVazio()
}

async function salvar() {
  if (!form.value.proprietario || !form.value.marca || !form.value.placa) {
    alert('Preencha todos os campos obrigatórios!')
    return
  }
  salvando.value = true
  try {
    if (editando.value) {
      await veiculosAPI.atualizar(editando.value.id, form.value)
    } else {
      await veiculosAPI.criar(form.value)
    }
    await carregar()
    fecharModal()
  } catch (e) {
    alert('Erro ao salvar: ' + (e.response?.data ? JSON.stringify(e.response.data) : e.message))
  }
  salvando.value = false
}

async function deletar(veiculo) {
  if (!confirm(`Deseja excluir o veículo ${veiculo.placa}?`)) return
  await veiculosAPI.deletar(veiculo.id)
  await carregar()
}

onMounted(carregar)
</script>