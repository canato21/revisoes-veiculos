import axios from 'axios'

const api = axios.create({
    baseURL: ' https://unadventuring-braiden-preauricular.ngrok-free.dev',
    headers: {
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': 'true'
    }
})

export const pessoasAPI = {
    listar: () => api.get('/pessoas/'),
    buscar: (id) => api.get(`/pessoas/${id}/`),
    criar: (dados) => api.post('/pessoas/', dados),
    atualizar: (id, dados) => api.put(`/pessoas/${id}/`, dados),
    deletar: (id) => api.delete(`/pessoas/${id}/`),
    porSexo: () => api.get('/pessoas/por-sexo/'),
}

export const veiculosAPI = {
    listar: () => api.get('/veiculos/'),
    buscar: (id) => api.get(`/veiculos/${id}/`),
    criar: (dados) => api.post('/veiculos/', dados),
    atualizar: (id, dados) => api.put(`/veiculos/${id}/`, dados),
    deletar: (id) => api.delete(`/veiculos/${id}/`),
    porPessoa: () => api.get('/veiculos/por-pessoa/'),
    porMarca: () => api.get('/veiculos/por-marca/'),
    quemTemMais: () => api.get('/veiculos/quem-tem-mais/'),
    marcasPorSexo: () => api.get('/veiculos/marcas-por-sexo/'),
}

export const revisoesAPI = {
    listar: () => api.get('/revisoes/'),
    buscar: (id) => api.get(`/revisoes/${id}/`),
    criar: (dados) => api.post('/revisoes/', dados),
    atualizar: (id, dados) => api.put(`/revisoes/${id}/`, dados),
    deletar: (id) => api.delete(`/revisoes/${id}/`),
    porPeriodo: (ini, fim) => api.get(`/revisoes/por-periodo/?inicio=${ini}&fim=${fim}`),
    marcasMaisRevisoes: () => api.get('/revisoes/marcas-mais-revisoes/'),
    pessoasMaisRevisoes: () => api.get('/revisoes/pessoas-mais-revisoes/'),
    mediaTempo: () => api.get('/revisoes/media-tempo/'),
    proximasRevisoes: () => api.get('/revisoes/proximas-revisoes/'),
}