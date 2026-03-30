/**
 * Este arquivo centraliza todas as chamadas HTTP para a API Django.
 * Usamos o Axios, uma biblioteca JavaScript para fazer requisições HTTP.
 *
 * Por que centralizar aqui?
 *   - Um único lugar para configurar a URL base do backend
 *   - Um único lugar para adicionar o token JWT em todas as requisições
 *   - Um único lugar para tratar erros de autenticação
 *   - Facilita trocar a URL do backend (ex: de localhost para produção)
 */

import axios from 'axios'

/**
 * Instância do Axios configurada com URL base e headers padrão.
 * Todas as chamadas da API usam esta instância, não o axios diretamente.
 * Assim, as configurações abaixo se aplicam a TODAS as requisições.
 */
const api = axios.create({
    baseURL: 'http://localhost:8000/api', // URL base do backend Django
    headers: {
        'Content-Type': 'application/json'  // informa que enviamos JSON
    }
})


// ── INTERCEPTORS ──────────────────────────────────────────────────────────────
// Interceptors são funções executadas automaticamente antes/depois de
// cada requisição ou resposta. Funcionam como "middleware" do Axios.


/**
 * INTERCEPTOR DE REQUISIÇÃO
 * Executado ANTES de toda requisição ser enviada ao backend.
 * Adiciona o token JWT no header Authorization de forma automática,
 * para que não precisemos repetir isso em cada chamada de API.
 */
api.interceptors.request.use(config => {
    // Busca o token salvo no localStorage (salvo no login)
    const token = localStorage.getItem('token')

    if (token) {
        // Adiciona o header: Authorization: Bearer eyJhbGci...
        // O backend Django lê este header e identifica o usuário
        config.headers.Authorization = `Bearer ${token}`
    }

    // IMPORTANTE: sempre retorne o config (modificado ou não)
    return config
})

/**
 * INTERCEPTOR DE RESPOSTA
 * Executado DEPOIS de toda resposta recebida do backend.
 * Trata o erro 401 (Não Autorizado) — significa que o token expirou.
 */
api.interceptors.response.use(
    // Caso de sucesso: retorna a resposta sem modificação
    response => response,

    // Caso de erro: verifica se é 401 (token expirado/inválido)
    error => {
        if (error.response?.status === 401) {
            // O operador ?. (optional chaining) evita erro se response for undefined

            // Remove o token e o usuário do localStorage
            localStorage.removeItem('token')
            localStorage.removeItem('usuario')

            // Redireciona para a tela de login
            window.location.href = '/login'
        }

        // Propaga o erro para quem chamou a função (para tratar no try/catch)
        return Promise.reject(error)
    }
)


// ── APIs POR RECURSO ───────────────────────────────────────────────────────────
// Cada objeto exportado agrupa as funções relacionadas a um recurso da API.
// Cada função retorna uma Promise (promessa de resultado futuro).
// No Vue, usamos 'await' para esperar o resultado.


/**
 * API de Autenticação
 */
export const authAPI = {
    // POST /api/token/ → recebe { username, password }, retorna { access, refresh }
    login: (dados) => api.post('/token/', dados),
}


/**
 * API de Pessoas
 */
export const pessoasAPI = {

    // GET /api/pessoas/{id}/ → retorna uma pessoa específica
    buscar: (id) => api.get(`/pessoas/${id}/`),

    // POST /api/pessoas/ → cria uma nova pessoa (dados no body)
    criar: (dados) => api.post('/pessoas/', dados),

    // PUT /api/pessoas/{id}/ → atualiza todos os campos de uma pessoa
    atualizar: (id, dados) => api.put(`/pessoas/${id}/`, dados),

    // DELETE /api/pessoas/{id}/ → deleta uma pessoa
    deletar: (id) => api.delete(`/pessoas/${id}/`),

    // GET /api/pessoas/por-sexo/ → relatório: pessoas separadas por sexo
    porSexo: () => api.get('/pessoas/por-sexo/'),

    listar: (search = '') => api.get(`/pessoas/?search=${search}`),

    porIdade: (ini, fim) => api.get(`/pessoas/idade/?inicio=${ini}&fim=${fim}`)
}


/**
 * API de Veículos
 */
export const veiculosAPI = {
    buscar: (id) => api.get(`/veiculos/${id}/`),
    criar: (dados) => api.post('/veiculos/', dados),
    atualizar: (id, dados) => api.put(`/veiculos/${id}/`, dados),
    deletar: (id) => api.delete(`/veiculos/${id}/`),
    listar: (search = '', proprietario = '') => {
        let url = '/veiculos/?'
        if (search) url += `search=${search}&`
        if (proprietario) url += `proprietario=${proprietario}&`
        return api.get(url)
    },

    // Relatórios de veículos
    porPessoa: () => api.get('/veiculos/por-pessoa/'),     // agrupados por pessoa
    porMarca: () => api.get('/veiculos/por-marca/'),      // por quantidade de marca
    quemTemMais: () => api.get('/veiculos/quem-tem-mais/'),  // homens vs mulheres
    marcasPorSexo: () => api.get('/veiculos/marcas-por-sexo/'), // marcas por sexo
}


/**
 * API de Revisões
 */
export const revisoesAPI = {
    listar: (veiculoId = '', search = '') => {
        const params = new URLSearchParams()
        if (veiculoId) params.append('veiculo', veiculoId)
        if (search) params.append('search', search)
        const query = params.toString()
        return api.get(`/revisoes/${query ? '?' + query : ''}`)
    },
    buscar: (id) => api.get(`/revisoes/${id}/`),
    criar: (dados) => api.post('/revisoes/', dados),
    atualizar: (id, dados) => api.put(`/revisoes/${id}/`, dados),
    deletar: (id) => api.delete(`/revisoes/${id}/`),

    // Relatórios de revisões
    // Template literals (`...`): permitem inserir variáveis na string com ${}
    porPeriodo: (ini, fim) => api.get(`/revisoes/por-periodo/?inicio=${ini}&fim=${fim}`),
    marcasMaisRevisoes: () => api.get('/revisoes/marcas-mais-revisoes/'),
    pessoasMaisRevisoes: () => api.get('/revisoes/pessoas-mais-revisoes/'),
    mediaTempo: () => api.get('/revisoes/media-tempo/'),
    proximasRevisoes: () => api.get('/revisoes/proximas-revisoes/'),
    porOficina: () => api.get('/revisoes/revisoes-oficina/'),
    buscarOficinas: (termo) => api.get(`/revisoes/?search=${termo}`)

}

export { api }
