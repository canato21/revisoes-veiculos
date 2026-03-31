/**
 * Este arquivo centraliza todas as chamadas HTTP para a API Django.
 * Usamos o Axios, uma biblioteca JavaScript para fazer requisições HTTP.
 */

import axios from 'axios'

/**
 * Instância do Axios configurada com URL base e headers padrão.
 */
const api = axios.create({
    baseURL: 'http://18.220.94.209:8000/api/', // URL base do seu servidor na AWS
    headers: {
        'Content-Type': 'application/json'
    }
})


// ── INTERCEPTORS ──────────────────────────────────────────────────────────────

/**
 * INTERCEPTOR DE REQUISIÇÃO
 * Adiciona o token JWT automaticamente em todas as chamadas.
 */
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

/**
 * INTERCEPTOR DE RESPOSTA
 * Trata erro 401 (token expirado) redirecionando para o login.
 */
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token')
            localStorage.removeItem('usuario')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)


// ── APIs POR RECURSO ───────────────────────────────────────────────────────────

/**
 * API de Autenticação
 */
export const authAPI = {
    login: (dados) => api.post('/token/', dados),
}


/**
 * API de Pessoas
 */
export const pessoasAPI = {
    buscar: (id) => api.get(`/pessoas/${id}/`),
    criar: (dados) => api.post('/pessoas/', dados),
    atualizar: (id, dados) => api.put(`/pessoas/${id}/`, dados),
    deletar: (id) => api.delete(`/pessoas/${id}/`),
    listar: (search = '') => api.get(`/pessoas/?search=${search}`),

    // Relatórios
    porSexo: () => api.get('/pessoas/por-sexo/'),
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

    // 🚀 NOVO MÉTODO DE RESUMO (Otimização para o Dashboard)
    resumo: () => api.get('/veiculos/resumo/'),

    // Outros Relatórios
    porPessoa: () => api.get('/veiculos/por-pessoa/'),
    porMarca: () => api.get('/veiculos/por-marca/'),
    quemTemMais: () => api.get('/veiculos/quem-tem-mais/'),
    marcasPorSexo: () => api.get('/veiculos/marcas-por-sexo/'),
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
    porPeriodo: (ini, fim) => api.get(`/revisoes/por-periodo/?inicio=${ini}&fim=${fim}`),
    marcasMaisRevisoes: () => api.get('/revisoes/marcas-mais-revisoes/'),
    pessoasMaisRevisoes: () => api.get('/revisoes/pessoas-mais-revisoes/'),
    mediaTempo: () => api.get('/revisoes/media-tempo/'),
    proximasRevisoes: () => api.get('/revisoes/proximas-revisoes/'),

    // 🚀 MÉTODO DE OFICINAS (Usado no Dashboard)
    porOficina: () => api.get('/revisoes/revisoes-oficina/'),

    buscarOficinas: (termo) => api.get(`/revisoes/?search=${termo}`)
}

export default api; // Exportação padrão da instância