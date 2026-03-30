<!--
  Esta é a única tela pública do sistema (meta.publico: true no router).
  O usuário informa usuário e senha, que são enviados ao backend Django.
  O backend valida e retorna um token JWT que é salvo no localStorage.
-->

<template>
  <!-- Centraliza o card na tela usando flexbox -->
  <div class="login-page">
    <div class="login-card">

      <!-- Logo e título -->
      <div class="login-logo">
        <div class="logo-icon">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10l2 2m0 0h10m-10 0V6m10 10l2-2V9.5a2 2 0 00-.586-1.414l-3.5-3.5A2 2 0 0016.5 4H13" />
          </svg>
        </div>
        <h1>AutoRevisão</h1>
        <p>Sistema de controle de revisões</p>
      </div>

      <!--
        @submit.prevent="entrar": ao enviar o form, chama entrar() e previne
        o comportamento padrão do HTML (que recarregaria a página).
        .prevent é um modificador de evento do Vue.
      -->
      <form @submit.prevent="entrar">

        <div class="form-group">
          <label>Usuário</label>
          <!--
            v-model="form.username": ligação bidirecional — quando o usuário
            digita, form.username atualiza; quando form.username muda, o input atualiza.
            :class="{ 'input-erro': erro }": adiciona classe CSS de erro se houver erro.
            autocomplete: sugere ao navegador preencher automaticamente.
          -->
          <input v-model="form.username" placeholder="Digite seu usuário" :class="{ 'input-erro': erro }"
            autocomplete="username" />
        </div>

        <div class="form-group">
          <label>Senha</label>
          <input v-model="form.password" type="password" placeholder="Digite sua senha" :class="{ 'input-erro': erro }"
            autocomplete="current-password" />
        </div>

        <!-- Mensagem de erro exibida quando o login falha -->
        <!-- v-if="erro": só renderiza este elemento se 'erro' tiver valor -->
        <span class="msg-erro" v-if="erro" style="margin-bottom:12px; display:block;">
          {{ erro }}
        </span>

        <!--
          type="submit": ao clicar, dispara o @submit.prevent do form acima.
          :disabled="carregando": desabilita o botão enquanto aguarda a resposta.
          O operador ternário: condição ? valor_se_true : valor_se_false
        -->
        <button type="submit" class="btn btn-primary" style="width:100%; justify-content:center; padding:11px;"
          :disabled="carregando">
          {{ carregando ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../services/api'

// useRouter(): permite navegar programaticamente (redirecionar)
const router = useRouter()

// Estado reativo da tela
const carregando = ref(false) // true enquanto aguarda resposta do backend
const erro = ref('')    // mensagem de erro (vazia = sem erro)

// Objeto que guarda os campos do formulário
// ref({ ... }): reatividade em objetos — qualquer mudança re-renderiza o template
const form = ref({
  username: '',
  password: ''
})

/**
 * Função chamada ao submeter o formulário.
 * async/await: permite código assíncrono de forma legível (sem .then().catch())
 */
async function entrar() {
  // Validação básica antes de chamar a API
  if (!form.value.username || !form.value.password) {
    erro.value = 'Preencha usuário e senha'
    return  // interrompe a execução
  }

  carregando.value = true
  erro.value = ''  // limpa erros anteriores

  try {
    // Chama POST /api/token/ com usuário e senha
    // await: espera a resposta antes de continuar
    const res = await authAPI.login(form.value)

    // Salva o token JWT no localStorage do navegador
    // O token é enviado em toda requisição futura (ver interceptor em api.js)
    localStorage.setItem('token', res.data.access)

    // Salva o nome do usuário para exibir na topbar
    localStorage.setItem('usuario', form.value.username)

    // Redireciona para o dashboard após login bem-sucedido
    router.push('/')

  } catch (e) {
    // Se o backend retornar erro (usuário/senha incorretos), exibe mensagem
    erro.value = 'Usuário ou senha incorretos'
  }

  carregando.value = false
}
</script>

<!-- scoped: este CSS só se aplica a este componente, não vaza para outros -->
<style scoped>
.login-page {
  min-height: 100vh;
  background: var(--gray-50);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: var(--radius-xl);
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--gray-100);
}

.login-logo {
  text-align: center;
  margin-bottom: 32px;
}

.login-logo .logo-icon {
  width: 52px;
  height: 52px;
  margin: 0 auto 14px;
  background: var(--primary);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-logo .logo-icon svg {
  width: 26px;
  height: 26px;
  color: white;
}

.login-logo h1 {
  font-size: 22px;
  font-weight: 700;
  color: var(--gray-900);
  letter-spacing: -0.3px;
}

.login-logo p {
  font-size: 13px;
  color: var(--gray-400);
  margin-top: 4px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
