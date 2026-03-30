<template>
    <div class="modal-overlay" @click.self="$emit('fechar')">
        <div class="modal" style="max-width:650px;">

            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <h3>Revisões: {{ veiculo?.marca }} {{ veiculo?.modelo }} ({{ veiculo?.placa }})</h3>
                <button v-if="exibindoFormulario" class="btn btn-ghost btn-sm"
                    @click="semHistorico ? $emit('fechar') : voltarParaLista()">
                    ← Voltar
                </button>
                <button v-else class="btn btn-primary btn-sm" @click="novaRevisao">
                    + Nova Revisão
                </button>
            </div>

            <!-- ── LISTA DE REVISÕES ─────────────────────────────────────── -->
            <div v-if="!exibindoFormulario">
                <div v-if="carregando" class="loading">Buscando histórico...</div>
                <table v-else-if="revisoes.length > 0">
                    <thead>
                        <tr>
                            <th>Data</th>
                            <th>KM</th>
                            <th>Oficina</th>
                            <th>Valor</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="rev in revisoes" :key="rev.id">
                            <td>{{ formatarData(rev.data_revisao) }}</td>
                            <td>{{ Number(rev.kilometragem).toLocaleString('pt-BR') }} km</td>
                            <td><span class="texto-truncado" style="max-width:120px; display:inline-block;">{{
                                    rev.oficina }}</span></td>
                            <td>{{ formatarValor(rev.valor) }}</td>
                            <td>
                                <button class="btn-icone" title="Editar" @click="editarRevisao(rev)">✏️</button>
                                <button class="btn-icone btn-icone-perigo" title="Excluir"
                                    @click="confirmarExclusao(rev)">🗑️</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div v-else style="text-align:center; color:var(--gray-500); padding:20px;">
                    Nenhuma revisão registrada para este veículo.
                </div>
            </div>

            <!-- ── FORMULÁRIO ───────────────────────────────────────────── -->
            <div v-else style="display:flex; flex-direction:column; gap:16px;">

                <!-- Linha 1: Data + KM -->
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">

                    <!-- Data -->
                    <div class="form-group" style="margin:0;" v-if="editandoId">
                        <label>Data</label>
                        <input type="date" v-model="form.data_revisao" :class="{ 'input-erro': erros.data_revisao }"
                            :min="dataMinima || undefined" :max="dataHoje" @input="delete erros.data_revisao" />
                        <div style="min-height:18px; margin-top:3px;">
                            <span class="msg-erro" v-if="erros.data_revisao">{{ erros.data_revisao }}</span>
                            <span v-else-if="dataMinima" style="font-size:11px; color:var(--gray-400);">
                                Mín: {{ formatarData(dataMinima) }} (revisão anterior)
                            </span>
                        </div>
                    </div>
                    <div class="form-group" style="margin:0;" v-else>
                        <label>Data</label>
                        <input :value="formatarData(form.data_revisao)" readonly
                            style="background:var(--gray-100); color:var(--gray-500); cursor:not-allowed;" />
                        <div style="min-height:18px; margin-top:3px;">
                            <span style="font-size:11px; color:var(--gray-400);">Preenchida automaticamente</span>
                        </div>
                    </div>

                    <!-- KM -->
                    <div class="form-group" style="margin:0;">
                        <label>Quilometragem (Máx 999.999.999)</label>
                        <input :value="kmFormatado" placeholder="Ex: 45.000" inputmode="numeric"
                            :class="{ 'input-erro': erros.kilometragem }" @input="aplicarMascaraKm" />
                        <div style="min-height:18px; margin-top:3px;">
                            <span class="msg-erro" v-if="erros.kilometragem">{{ erros.kilometragem }}</span>
                            <span v-else-if="kmMinimo" style="font-size:11px; color:var(--gray-400);">
                                Mín: {{ Number(kmMinimo).toLocaleString('pt-BR') }} km (revisão anterior)
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Linha 2: Oficina (largura total) -->
                <div class="form-group" style="margin:0;">
                    <label>Oficina</label>

                    <div style="display:flex; gap:8px;">
                        <!-- Input + dropdown -->
                        <div style="position:relative; flex:1;">
                            <input v-model="form.oficina" maxlength="100" placeholder="Digite para buscar..."
                                :class="{ 'input-erro': erros.oficina }" autocomplete="off" @input="aoDigitarOficina"
                                @focus="dropdownAberto = true" @blur="aoSairCampoOficina" />
                            <!-- Dropdown -->
                            <ul v-if="dropdownAberto && form.oficina && form.oficina.length >= 2" style="position:absolute; top:100%; left:0; right:0; background:#fff;
                                       border:1.5px solid var(--gray-200); border-top:none;
                                       border-radius:0 0 8px 8px; z-index:50; max-height:200px;
                                       overflow-y:auto; list-style:none; padding:0; margin:0;
                                       box-shadow:0 4px 12px rgba(0,0,0,.10);">
                                <li v-if="buscandoOficinas"
                                    style="padding:10px 14px; color:var(--gray-500); font-size:13px; text-align:center;">
                                    Buscando...
                                </li>
                                <template v-else>
                                    <li v-if="oficinasSugeridas.length === 0"
                                        style="padding:10px 14px; color:var(--gray-400); font-size:13px; text-align:center;">
                                        Nenhuma oficina encontrada
                                    </li>
                                    <li v-for="of in oficinasSugeridas" :key="of"
                                        @mousedown.prevent="selecionarOficina(of)" style="padding:10px 14px; cursor:pointer; font-size:13px;
                                               color:var(--gray-700); border-bottom:1px solid var(--gray-100);"
                                        onmouseover="this.style.backgroundColor='var(--gray-100)'"
                                        onmouseout="this.style.backgroundColor='#fff'">
                                        {{ of }}
                                    </li>
                                </template>
                            </ul>
                        </div>
                        <!-- Botão + -->
                        <button type="button" class="btn btn-primary" title="Cadastrar nova oficina"
                            style="padding:0 14px; height:40px; flex-shrink:0; font-size:20px; line-height:1;"
                            @click="abrirCadastroOficina">+</button>
                    </div>

                    <!-- Rodapé do campo: erro à esquerda, contador à direita -->
                    <div
                        style="display:flex; justify-content:space-between; align-items:center; margin-top:3px; min-height:18px;">
                        <span class="msg-erro" v-if="erros.oficina">{{ erros.oficina }}</span>
                        <span v-else></span>
                        <small style="color:var(--gray-400);">{{ form.oficina?.length || 0 }}/100</small>
                    </div>

                    <!-- Mini-form nova oficina -->
                    <div v-if="cadastrandoOficina" style="margin-top:8px; background:#f8fafc; border:1.5px solid var(--primary);
                               border-radius:8px; padding:14px;">
                        <p style="font-size:13px; font-weight:600; color:var(--gray-700); margin:0 0 10px;">
                            Nova oficina
                        </p>
                        <div style="display:flex; gap:8px; align-items:center;">
                            <input v-model="novaOficinaNome" maxlength="100" placeholder="Nome da nova oficina" style="flex:1; padding:8px 12px; border:1.5px solid var(--gray-200);
                                       border-radius:7px; font-size:13px; outline:none;"
                                @keyup.enter="confirmarNovaOficina"
                                @focus="$event.target.style.borderColor = 'var(--primary)'"
                                @blur="$event.target.style.borderColor = 'var(--gray-200)'" ref="inputNovaOficina" />
                            <button class="btn btn-ghost btn-sm" type="button"
                                @click="cancelarCadastroOficina">Cancelar</button>
                            <button class="btn btn-primary btn-sm" type="button" @click="confirmarNovaOficina"
                                :disabled="!novaOficinaNome.trim()">Adicionar</button>
                        </div>
                        <span v-if="erroNovaOficina" class="msg-erro" style="display:block; margin-top:6px;">
                            {{ erroNovaOficina }}
                        </span>
                    </div>
                </div>

                <!-- Linha 3: Valor -->
                <div class="form-group" style="margin:0;">
                    <label>Valor (Máx R$ 999.999,99)</label>
                    <input v-model="valorFormatado" placeholder="R$ 0,00" :class="{ 'input-erro': erros.valor }"
                        @input="aplicarMascara" />
                    <div style="min-height:18px; margin-top:3px;">
                        <span class="msg-erro" v-if="erros.valor">{{ erros.valor }}</span>
                    </div>
                </div>

                <!-- Linha 4: Descrição -->
                <div class="form-group" style="margin:0;">
                    <label>Descrição do Serviço</label>
                    <textarea v-model="form.descricao" maxlength="500" rows="3" placeholder="O que foi feito?"
                        :class="{ 'input-erro': erros.descricao }" @input="delete erros.descricao"></textarea>
                    <div
                        style="display:flex; justify-content:space-between; align-items:center; margin-top:3px; min-height:18px;">
                        <span class="msg-erro" v-if="erros.descricao">{{ erros.descricao }}</span>
                        <span v-else></span>
                        <small style="color:var(--gray-400);">{{ form.descricao?.length || 0 }}/500</small>
                    </div>
                </div>

                <!-- Salvar -->
                <button class="btn btn-primary" @click="salvar" :disabled="salvando"
                    style="width:100%; justify-content:center; padding:11px; margin-top:4px;">
                    {{ salvando ? 'Salvando...' : 'Salvar Revisão' }}
                </button>

            </div>
        </div>
    </div>

    <!-- ── MODAL DE EXCLUSÃO ─────────────────────────────────────────────── -->
    <div class="modal-overlay" v-if="modalExclusaoAberto" @click.self="modalExclusaoAberto = false"
        style="z-index:9999;">
        <div class="modal" style="max-width:420px;">
            <div style="text-align:center; padding:8px 0 20px;">
                <div style="font-size:48px; margin-bottom:12px;">⚠️</div>
                <h3 style="margin-bottom:8px;">Confirmar exclusão</h3>
                <p style="color:var(--gray-500); font-size:14px;">
                    Deseja excluir a revisão do dia
                    <strong>{{ formatarData(revisaoParaExcluir?.data_revisao) }}</strong>
                    no valor de <strong>{{ formatarValor(revisaoParaExcluir?.valor) }}</strong>?
                    <br><br>Esta ação não pode ser desfeita.
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
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { revisoesAPI } from '../services/api'

const props = defineProps({
    veiculo: { type: Object, required: true },
    iniciarNovo: { type: Boolean, default: false },
    semHistorico: { type: Boolean, default: false }
})
const emit = defineEmits(['fechar'])

// ── ESTADOS GERAIS ─────────────────────────────────────────────────────────
const revisoes = ref([])
const carregando = ref(false)
const exibindoFormulario = ref(false)
const salvando = ref(false)
const erros = ref({})
const valorFormatado = ref('')
const kmFormatado = ref('')   // exibição formatada (ex: "45.000")
const editandoId = ref(null)

const modalExclusaoAberto = ref(false)
const revisaoParaExcluir = ref(null)
const excluindo = ref(false)

// ── AUTOCOMPLETE DE OFICINA ────────────────────────────────────────────────
const oficinasSugeridas = ref([])
const buscandoOficinas = ref(false)
const dropdownAberto = ref(false)
// Guarda os nomes que vieram do banco na última busca (para validação no blur)
const oficinasConhecidas = ref([])
let timeoutBusca = null

function aoDigitarOficina() {
    delete erros.value.oficina
    dropdownAberto.value = true
    clearTimeout(timeoutBusca)

    if (!form.value.oficina || form.value.oficina.length < 2) {
        oficinasSugeridas.value = []
        oficinasConhecidas.value = []
        return
    }

    timeoutBusca = setTimeout(async () => {
        buscandoOficinas.value = true
        try {
            const res = await revisoesAPI.buscarOficinas(form.value.oficina)
            const lista = res.data.results || res.data
            const nomes = [...new Set(lista.map(r => r.oficina || r).filter(Boolean))]
            oficinasSugeridas.value = nomes
            oficinasConhecidas.value = nomes
        } catch (e) {
            console.error('Erro ao buscar oficinas:', e)
        }
        buscandoOficinas.value = false
    }, 300)
}

function aoSairCampoOficina() {
    // Aguarda um tick para que o mousedown do item do dropdown seja processado antes
    setTimeout(() => {
        dropdownAberto.value = false

        const digitado = form.value.oficina?.trim() ?? ''
        if (!digitado) return // deixa a validação do submit cuidar disso

        // Se o que foi digitado não bate com nenhuma oficina conhecida → erro
        const existe = oficinasConhecidas.value.some(
            o => o.toLowerCase() === digitado.toLowerCase()
        )
        if (!existe) {
            erros.value.oficina =
                'Oficina não encontrada. Selecione uma da lista ou clique em "+" para cadastrar.'
        }
    }, 160)
}

function selecionarOficina(nome) {
    form.value.oficina = nome
    dropdownAberto.value = false
    oficinasSugeridas.value = []
    delete erros.value.oficina
}

// ── CADASTRO DE NOVA OFICINA (inline) ─────────────────────────────────────
const cadastrandoOficina = ref(false)
const novaOficinaNome = ref('')
const erroNovaOficina = ref('')
const inputNovaOficina = ref(null)

function abrirCadastroOficina() {
    // Pré-preenche com o que já foi digitado no campo, se houver
    novaOficinaNome.value = form.value.oficina?.trim() ?? ''
    erroNovaOficina.value = ''
    cadastrandoOficina.value = true
    nextTick(() => inputNovaOficina.value?.focus())
}

function cancelarCadastroOficina() {
    cadastrandoOficina.value = false
    novaOficinaNome.value = ''
    erroNovaOficina.value = ''
}

async function confirmarNovaOficina() {
    const nome = novaOficinaNome.value.trim()
    if (!nome) return

    // Verifica se já existe exatamente no banco (busca exata)
    try {
        const res = await revisoesAPI.buscarOficinas(nome)
        const lista = res.data.results || res.data
        const nomes = lista.map(r => (r.oficina || r).toLowerCase())
        if (nomes.includes(nome.toLowerCase())) {
            erroNovaOficina.value = `A oficina "${nome}" já está cadastrada. Selecione-a na lista.`
            return
        }
    } catch (e) {
        console.error(e)
    }

    // Aceita o nome novo: coloca no campo e atualiza a lista de conhecidas
    selecionarOficina(nome)
    oficinasConhecidas.value = [...oficinasConhecidas.value, nome]
    cancelarCadastroOficina()
}

// ── LÓGICA DO FORMULÁRIO ───────────────────────────────────────────────────
const dataHoje = computed(() => new Date().toISOString().split('T')[0])

const formVazio = () => ({
    id: null, veiculo: null,
    data_revisao: '', kilometragem: '', oficina: '', valor: 0, descricao: ''
})
const form = ref(formVazio())

const ultimaRevisao = computed(() => {
    if (revisoes.value.length === 0) return null
    const ordenada = [...revisoes.value].sort((a, b) => new Date(b.data_revisao) - new Date(a.data_revisao))
    if (!editandoId.value) return ordenada[0]
    const idx = ordenada.findIndex(r => r.id === editandoId.value)
    return idx < ordenada.length - 1 ? ordenada[idx + 1] : null
})

const kmMinimo = computed(() => ultimaRevisao.value ? Number(ultimaRevisao.value.kilometragem) : null)
const dataMinima = computed(() => ultimaRevisao.value ? ultimaRevisao.value.data_revisao : null)

onMounted(async () => {
    await buscarRevisoes()
    if (props.iniciarNovo) {
        exibindoFormulario.value = true
        form.value = formVazio()
        form.value.veiculo = props.veiculo.id
        form.value.data_revisao = dataHoje.value
        valorFormatado.value = ''
        kmFormatado.value = ''
        erros.value = {}
    }
})

async function buscarRevisoes() {
    carregando.value = true
    try {
        const res = await revisoesAPI.listar(props.veiculo.id)
        revisoes.value = res.data.results || res.data
    } catch (e) { console.error(e) }
    carregando.value = false
}

function novaRevisao() {
    editandoId.value = null
    form.value = formVazio()
    form.value.veiculo = props.veiculo.id
    form.value.data_revisao = dataHoje.value
    valorFormatado.value = ''
    kmFormatado.value = ''
    erros.value = {}
    oficinasConhecidas.value = []
    oficinasSugeridas.value = []
    dropdownAberto.value = false
    cadastrandoOficina.value = false
    exibindoFormulario.value = true
}

function editarRevisao(rev) {
    editandoId.value = rev.id
    form.value = { ...rev }
    valorFormatado.value = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(rev.valor)
    kmFormatado.value = rev.kilometragem ? Number(rev.kilometragem).toLocaleString('pt-BR') : ''
    erros.value = {}
    // Marca a oficina atual como conhecida para não disparar erro no blur
    oficinasConhecidas.value = rev.oficina ? [rev.oficina] : []
    oficinasSugeridas.value = []
    dropdownAberto.value = false
    cadastrandoOficina.value = false
    exibindoFormulario.value = true
}

function voltarParaLista() {
    exibindoFormulario.value = false
    editandoId.value = null
    erros.value = {}
    cadastrandoOficina.value = false
}

// KM: máscara com separador de milhar, limite 999.999.999
function aplicarMascaraKm(event) {
    // Extrai só dígitos e limita a 9 caracteres imediatamente
    const soNumeros = event.target.value.replace(/\D/g, '').slice(0, 9)
    const numero = soNumeros ? parseInt(soNumeros, 10) : null
    form.value.kilometragem = numero

    // Formata e reescreve o valor visível no input (força o limite visualmente)
    const formatado = numero !== null ? numero.toLocaleString('pt-BR') : ''
    kmFormatado.value = formatado
    event.target.value = formatado  // reescreve direto no DOM

    delete erros.value.kilometragem
}

function aplicarMascara(event) {
    let soNumeros = event.target.value.replace(/\D/g, '')
    if (!soNumeros) { valorFormatado.value = ''; form.value.valor = 0; return }
    if (soNumeros.length > 8) soNumeros = soNumeros.slice(0, 8)
    const dec = (parseInt(soNumeros) / 100).toFixed(2)
    form.value.valor = dec
    valorFormatado.value = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(dec)
    delete erros.value.valor
}

function validar() {
    erros.value = {}

    if (editandoId.value) {
        if (!form.value.data_revisao)
            erros.value.data_revisao = 'Data é obrigatória'
        else if (form.value.data_revisao > dataHoje.value)
            erros.value.data_revisao = 'Data não pode ser no futuro'
        else if (dataMinima.value && form.value.data_revisao < dataMinima.value)
            erros.value.data_revisao = `Data não pode ser anterior à revisão passada (${formatarData(dataMinima.value)})`
    }

    if (!form.value.kilometragem || form.value.kilometragem <= 0)
        erros.value.kilometragem = 'Informe a KM'
    else if (form.value.kilometragem > 999999999)
        erros.value.kilometragem = 'KM máxima é 999.999.999'
    else if (kmMinimo.value !== null && Number(form.value.kilometragem) < kmMinimo.value)
        erros.value.kilometragem = `KM não pode ser menor que a revisão passada (${Number(kmMinimo.value).toLocaleString('pt-BR')} km)`

    if (!form.value.oficina || form.value.oficina.trim().length < 2)
        erros.value.oficina = 'Oficina é obrigatória'

    if (!form.value.valor || form.value.valor <= 0)
        erros.value.valor = 'Informe um valor válido'
    else if (parseFloat(form.value.valor) > 999999.99)
        erros.value.valor = 'Valor máximo é R$ 999.999,99'

    if (!form.value.descricao || form.value.descricao.trim().length < 5)
        erros.value.descricao = 'Descrição muito curta (mínimo 5 caracteres)'

    return Object.keys(erros.value).length === 0
}

async function salvar() {
    if (!validar()) return
    salvando.value = true
    try {
        if (form.value.id) await revisoesAPI.atualizar(form.value.id, form.value)
        else await revisoesAPI.criar(form.value)

        if (props.semHistorico) emit('fechar')
        else { await buscarRevisoes(); voltarParaLista() }
    } catch (e) { console.error(e) }
    salvando.value = false
}

function confirmarExclusao(rev) { revisaoParaExcluir.value = rev; modalExclusaoAberto.value = true }

async function deletar() {
    excluindo.value = true
    try {
        await revisoesAPI.deletar(revisaoParaExcluir.value.id)
        await buscarRevisoes()
        modalExclusaoAberto.value = false
        revisaoParaExcluir.value = null
    } catch (e) { console.error(e) }
    excluindo.value = false
}

function formatarData(data) {
    if (!data) return '-'
    const [y, m, d] = data.split('-')
    return `${d}/${m}/${y}`
}
function formatarValor(valor) {
    return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}
</script>