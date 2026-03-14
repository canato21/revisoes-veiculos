<template>
  <div class="fade-in">
    <div class="page-header">
      <h1>👥 Pessoas</h1>
      <p>Cadastro e gerenciamento de proprietários</p>
    </div>

    <div class="table-container">
      <div class="table-header">
        <h3>{{ pessoas.length }} pessoas cadastradas</h3>
        <button class="btn btn-primary" @click="abrirModal()">+ Nova Pessoa</button>
      </div>

      <div v-if="carregando" class="loading">Carregando...</div>

      <table v-else>
        <thead>
          <tr>
            <th>Nome</th>
            <th>CPF</th>
            <th>Email</th>
            <th>Telefone</th>
            <th>Sexo</th>
            <th>Nascimento</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in pessoas" :key="p.id" class="fade-in">
            <td><strong>{{ p.nome }}</strong></td>
            <td>{{ p.cpf }}</td>
            <td>{{ p.email }}</td>
            <td>{{ p.telefone }}</td>
            <td>
              <span class="badge" :class="p.sexo === 'M' ? 'badge-m' : 'badge-f'">
                {{ p.sexo === 'M' ? 'Masculino' : 'Feminino' }}
              </span>
            </td>
            <td>{{ formatarData(p.data_nascimento) }}</td>
            <td>
              <button class="btn btn-warning btn-sm" @click="abrirModal(p)">✏️ Editar</button>
              <button class="btn btn-danger btn-sm" style="margin-left:6px" @click="deletar(p)">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div class="modal-overlay" v-if="modalAberto" @click.self="fecharModal">
      <div class="modal">
        <h3>{{ editando ? '✏️ Editar Pessoa' : '➕ Nova Pessoa' }}</h3>
        <div class="form-grid">
          <div class="form-group full">
            <label>Nome completo</label>
            <input v-model="form.nome" placeholder="Ex: João Silva" />
          </div>
          <div class="form-group">
            <label>CPF</label>
            <input v-model="form.cpf" placeholder="000.000.000-00" />
          </div>
          <div class="form-group">
            <label>Telefone</label>
            <input v-model="form.telefone" placeholder="(67) 99999-9999" />
          </div>
          <div class="form-group full">
            <label>Email</label>
            <input v-model="form.email" type="email" placeholder="email@exemplo.com" />
          </div>
          <div class="form-group">
            <label>Data de Nascimento</label>
            <input v-model="form.data_nascimento" type="date" />
          </div>
          <div class="form-group">
            <label>Sexo</label>
            <select v-model="form.sexo">
              <option value="">Selecione...</option>
              <option value="M">Masculino</option>
              <option value="F">Feminino</option>
            </select>
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
import { pessoasAPI } from '../services/api'

const pessoas     = ref([])
const carregando  = ref(true)
const modalAberto = ref(false)
const editando    = ref(null)
const salvando    = ref(false)

const formVazio = () => ({
  nome: '', cpf: '', email: '', telefone: '',
  data_nascimento: '', sexo: ''
})
const form = ref(formVazio())

function formatarData(data) {
  if (!data) return '-'
  const [y, m, d] = data.split('-')
  return `${d}/${m}/${y}`
}

async function carregar() {
  carregando.value = true
  const res = await pessoasAPI.listar()
  pessoas.value = res.data.results || res.data
  carregando.value = false
}

function abrirModal(pessoa = null) {
  editando.value = pessoa
  form.value = pessoa ? { ...pessoa } : formVazio()
  modalAberto.value = true
}

function fecharModal() {
  modalAberto.value = false
  editando.value = null
  form.value = formVazio()
}

async function salvar() {
  if (!form.value.nome || !form.value.cpf || !form.value.email || !form.value.sexo) {
    alert('Preencha todos os campos obrigatórios!')
    return
  }
  salvando.value = true
  try {
    if (editando.value) {
      await pessoasAPI.atualizar(editando.value.id, form.value)
    } else {
      await pessoasAPI.criar(form.value)
    }
    await carregar()
    fecharModal()
  } catch (e) {
    alert('Erro ao salvar: ' + (e.response?.data ? JSON.stringify(e.response.data) : e.message))
  }
  salvando.value = false
}

async function deletar(pessoa) {
  if (!confirm(`Deseja excluir ${pessoa.nome}?`)) return
  await pessoasAPI.deletar(pessoa.id)
  await carregar()
}

onMounted(carregar)
</script>