<template>
  <div class="fade-in">

    <div class="page-header">
      <h1>Pessoas</h1>
      <p>Cadastro e gerenciamento de proprietários</p>
    </div>

    <div class="table-container">

      <div class="table-header">
        <div>
          <h3>{{ totalPessoas }} pessoas cadastradas</h3>
        </div>
        <div style="display:flex; gap:10px; align-items:center;">
          <input v-model="busca" placeholder="Buscar por nome, CPF, email..."
            style="width:280px; padding:8px 12px; border:1.5px solid var(--gray-200); border-radius:var(--radius); font-size:13px; outline:none;"
            @focus="$event.target.style.borderColor = 'var(--primary)'"
            @blur="$event.target.style.borderColor = 'var(--gray-200)'" />
          <button class="btn btn-primary" @click="abrirModal()">+ Nova Pessoa</button>
        </div>
      </div>

      <div v-if="carregando" class="loading">Carregando...</div>

      <table v-else>
        <thead>
          <tr>
            <th style="min-width:140px;">Nome</th>
            <th style="min-width:130px;">CPF</th>
            <th style="min-width:180px;">Email</th>
            <th>CEP</th>
            <th style="min-width:180px;">Endereço</th>
            <th style="min-width:120px;">Telefone</th>
            <th>Sexo</th>
            <th>Nasc.</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in pessoas" :key="p.id" class="fade-in">
            <td style="max-width:160px;">
              <strong class="texto-truncado">{{ p.nome }}</strong>
            </td>
            <td style="white-space:nowrap;">{{ p.cpf }}</td>
            <td style="max-width:200px;">
              <span class="texto-truncado" :title="p.email">{{ p.email }}</span>
            </td>
            <td style="white-space:nowrap;">{{ p.cep || '—' }}</td>
            <td style="max-width:220px;">
              <span class="texto-truncado" v-if="p.rua"
                :title="p.rua + (p.numero ? ', ' + p.numero : '') + (p.bairro ? ' — ' + p.bairro : '')">
                {{ p.rua }}{{ p.numero ? ', ' + p.numero : '' }}
                <span style="color:var(--gray-400); font-size:12px;" v-if="p.bairro"> — {{ p.bairro }}</span>
              </span>
              <span v-else style="color:var(--gray-400);">—</span>
            </td>
            <td style="white-space:nowrap;">{{ p.telefone }}</td>
            <td>
              <span class="badge" :class="p.sexo === 'M' ? 'badge-m' : 'badge-f'">
                {{ p.sexo === 'M' ? 'M' : 'F' }}
              </span>
            </td>
            <td>{{ formatarData(p.data_nascimento) }}</td>
            <td>
              <div style="display:flex; gap:6px; align-items:center;">
                <button class="btn-icone" title="Veículos" @click="abrirModalVeiculo(p)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="1" y="3" width="15" height="13" rx="2" />
                    <path d="M16 8h4l3 5v3h-7V8z" />
                    <circle cx="5.5" cy="18.5" r="2.5" />
                    <circle cx="18.5" cy="18.5" r="2.5" />
                  </svg>
                </button>
                <button class="btn-icone" title="Editar" @click="abrirModal(p)">✏️</button>
                <button class="btn-icone btn-icone-perigo" title="Excluir" @click="confirmarExclusao(p)">🗑️</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div
        style="display:flex; justify-content:space-between; align-items:center; padding:14px 24px; border-top:1px solid var(--gray-100);">
        <span v-if="totalPessoas > 0" style="font-size:13px; color:var(--gray-500);">
          Mostrando {{ inicioPaginacao }} a {{ fimPaginacao }} de {{ totalPessoas }} pessoas
        </span>
        <span v-else style="font-size:13px; color:var(--gray-500);">Nenhuma pessoa encontrada</span>
        <div style="display:flex; gap:8px;">
          <button class="btn btn-ghost btn-sm" :disabled="!paginaAnterior" @click="carregar(paginaAnterior)">←
            Anterior</button>
          <button class="btn btn-ghost btn-sm" :disabled="!proximaPagina" @click="carregar(proximaPagina)">Próxima
            →</button>
        </div>
      </div>
    </div>
  </div>


  <div class="modal-overlay" v-if="modalExclusaoAberto" @click.self="modalExclusaoAberto = false">
    <div class="modal" style="max-width:420px;">
      <div style="text-align:center; padding:8px 0 20px;">
        <div style="font-size:48px; margin-bottom:12px;">⚠️</div>
        <h3 style="margin-bottom:8px;">Confirmar exclusão</h3>
        <p style="color:var(--gray-500); font-size:14px;">
          Deseja excluir <strong>{{ pessoaParaExcluir?.nome }}</strong>?
          Todos os veículos e revisões associados também serão removidos.
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


  <div class="modal-overlay" v-if="modalAberto" @click.self="fecharModal">
    <div class="modal">
      <h3>{{ editando ? 'Editar Pessoa' : 'Nova Pessoa' }}</h3>

      <div class="form-grid">

        <div class="form-group full">
          <label>Nome completo</label>
          <input v-model="form.nome" placeholder="Ex: João Silva" :class="{ 'input-erro': erros.nome }"
            @input="form.nome = form.nome.slice(0, 80); delete erros.nome" maxlength="80" />
          <div style="display:flex; justify-content:space-between;">
            <span class="msg-erro" v-if="erros.nome">{{ erros.nome }}</span>
            <span style="font-size:11px; color:var(--gray-400); margin-left:auto;">{{ form.nome.length }}/80</span>
          </div>
        </div>

        <div class="form-group">
          <label>CPF</label>
          <input v-model="form.cpf" placeholder="000.000.000-00" :class="{ 'input-erro': erros.cpf }"
            @input="form.cpf = formatarCPF(form.cpf); delete erros.cpf" maxlength="14" />
          <span class="msg-erro" v-if="erros.cpf">{{ erros.cpf }}</span>
        </div>

        <div class="form-group">
          <label>Telefone</label>
          <input v-model="form.telefone" placeholder="(67) 99999-9999" :class="{ 'input-erro': erros.telefone }"
            @input="form.telefone = formatarTelefone(form.telefone); delete erros.telefone" maxlength="15" />
          <span class="msg-erro" v-if="erros.telefone">{{ erros.telefone }}</span>
        </div>

        <div class="form-group full">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="email@exemplo.com"
            :class="{ 'input-erro': erros.email }" @input="form.email = form.email.slice(0, 100); delete erros.email"
            maxlength="100" />
          <div style="display:flex; justify-content:space-between;">
            <span class="msg-erro" v-if="erros.email">{{ erros.email }}</span>
            <span style="font-size:11px; color:var(--gray-400); margin-left:auto;">{{ form.email.length }}/100</span>
          </div>
        </div>

        <div class="form-group">
          <label>Data de Nascimento</label>
          <input v-model="form.data_nascimento" type="date" :max="dataMaximaNascimento" min="1900-01-01"
            :class="{ 'input-erro': erros.data_nascimento }" @input="delete erros.data_nascimento" />
          <span class="msg-erro" v-if="erros.data_nascimento">{{ erros.data_nascimento }}</span>
        </div>

        <div class="form-group">
          <label>Sexo</label>
          <div class="radio-grupo" :class="{ 'input-erro-radio': erros.sexo }">
            <label class="radio-opcao" :class="{ ativo: form.sexo === 'M' }">
              <input type="radio" value="M" v-model="form.sexo" @change="delete erros.sexo" />
              Masculino
            </label>
            <label class="radio-opcao" :class="{ ativo: form.sexo === 'F' }">
              <input type="radio" value="F" v-model="form.sexo" @change="delete erros.sexo" />
              Feminino
            </label>
          </div>
          <span class="msg-erro" v-if="erros.sexo">{{ erros.sexo }}</span>
        </div>

        <div class="form-group full">
          <div class="endereco-separador"><span>Endereço</span></div>
        </div>

        <div class="form-group">
          <label>CEP</label>
          <div class="cep-wrapper">
            <input v-model="form.cep" placeholder="00000-000" :class="{ 'input-erro': erros.cep }"
              @input="form.cep = formatarCEP(form.cep); delete erros.cep" @blur="buscarCEP" maxlength="9" />
            <span v-if="buscandoCEP" class="cep-spinner"></span>
            <span v-else-if="cepEncontrado" class="cep-ok">✓</span>
          </div>
          <span class="msg-erro" v-if="erros.cep">{{ erros.cep }}</span>
          <span class="cep-dica" v-if="!erros.cep">Preencha o CEP para autocompletar o endereço</span>
        </div>

        <div class="form-group">
          <label>Cidade / Estado</label>
          <input :value="form.cidade && form.estado ? `${form.cidade} — ${form.estado}` : ''"
            placeholder="Preenchido automaticamente" readonly class="input-readonly" />
        </div>

        <div class="form-group full">
          <label>Rua / Logradouro</label>
          <input v-model="form.rua" placeholder="Preenchido automaticamente pelo CEP"
            :class="{ 'input-erro': erros.rua }" @input="delete erros.rua" maxlength="200" />
          <span class="msg-erro" v-if="erros.rua">{{ erros.rua }}</span>
        </div>

        <div class="form-group">
          <label>Bairro</label>
          <input v-model="form.bairro" placeholder="Preenchido automaticamente pelo CEP"
            :class="{ 'input-erro': erros.bairro }" @input="delete erros.bairro" maxlength="100" />
          <span class="msg-erro" v-if="erros.bairro">{{ erros.bairro }}</span>
        </div>

        <div class="form-group">
          <label>Número</label>
          <input v-model="form.numero" placeholder="Ex: 123 ou S/N" :class="{ 'input-erro': erros.numero }"
            @input="form.numero = form.numero.replace(/[^a-zA-Z0-9\/]/g, '').slice(0, 10); delete erros.numero"
            maxlength="10" />
          <div style="display:flex; justify-content:space-between;">
            <span class="msg-erro" v-if="erros.numero">{{ erros.numero }}</span>
            <span style="font-size:11px; color:var(--gray-400); margin-left:auto;">{{ (form.numero || '').length
              }}/10</span>
          </div>
        </div>

      </div>

      <div class="modal-footer">
        <button class="btn btn-ghost" @click="fecharModal">Cancelar</button>
        <button class="btn btn-primary" @click="salvar" :disabled="salvando">
          {{ salvando ? 'Salvando...' : 'Salvar' }}
        </button>
      </div>
    </div>
  </div>


  <div class="modal-overlay" v-if="modalExclusaoVeiculoAberto" @click.self="modalExclusaoVeiculoAberto = false"
    style="z-index: 9999;">
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
        <button class="btn btn-ghost" @click="modalExclusaoVeiculoAberto = false">Cancelar</button>
        <button class="btn btn-danger" @click="deletarVeiculo" :disabled="excluindoVeiculo">
          {{ excluindoVeiculo ? 'Excluindo...' : 'Sim, excluir' }}
        </button>
      </div>
    </div>
  </div>


  <div class="modal-overlay" v-if="modalVeiculoNovoAberto" @click.self="fecharModalVeiculo">
    <div class="modal"
      style="max-width:980px; width:95vw; padding:0; overflow:hidden; border-radius:14px; position:relative;">

      <button class="modal-close" @click="fecharModalVeiculo"
        style="position:absolute; top:24px; right:24px; z-index:10; background:transparent; border:none; font-size:24px; color:var(--gray-400); cursor:pointer; line-height:1;">
        &times;
      </button>

      <div style="display:grid; grid-template-columns:1fr 1fr; min-height:550px;">

        <div
          style="padding:32px; border-right:1px solid var(--gray-100); overflow-y:auto; max-height:80vh; background:#fff;">

          <div style="margin-bottom: 24px;">
            <h3 style="margin:0; font-size:18px; font-weight:700; color:var(--gray-800);">
              Veículos de {{ pessoaSelecionada?.nome }}
            </h3>
            <p style="margin:5px 0 0; font-size:13px; color:var(--gray-500);">
              {{ veiculosDaPessoa.length }} veículo(s) cadastrado(s)
            </p>
          </div>

          <div v-if="carregandoVeiculos"
            style="display:flex; align-items:center; justify-content:center; height:140px; color:var(--gray-400); font-size:13px; gap:8px;">
            <svg style="animation:spin 1s linear infinite; opacity:.5" xmlns="http://www.w3.org/2000/svg" width="18"
              height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12a9 9 0 1 1-6.219-8.56" />
            </svg>
            Carregando veículos...
          </div>

          <div v-else-if="veiculosDaPessoa.length === 0"
            style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:220px; gap:14px; color:var(--gray-400); text-align:center;">
            <svg xmlns="http://www.w3.org/2000/svg" width="52" height="52" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"
              style="opacity:.25; color:var(--gray-500)">
              <rect x="1" y="3" width="15" height="13" rx="2" />
              <path d="M16 8h4l3 5v3h-7V8z" />
              <circle cx="5.5" cy="18.5" r="2.5" />
              <circle cx="18.5" cy="18.5" r="2.5" />
            </svg>
            <div>
              <p style="font-size:14px; font-weight:600; color:var(--gray-600); margin:0 0 4px;">Nenhum veículo ainda
              </p>
              <p style="font-size:12px; color:var(--gray-400); margin:0;">Preencha o formulário ao lado para adicionar o
                primeiro.</p>
            </div>
          </div>

          <div v-else style="display:flex; flex-direction:column; gap:14px;">
            <div v-for="v in veiculosDaPessoa" :key="v.id"
              style="border:1.5px solid var(--gray-150, #e8eaed); border-radius:12px; padding:18px 20px; background:#fff; transition:border-color .15s, box-shadow .15s;"
              :style="formVeiculo.id === v.id
                ? { borderColor: 'var(--primary)', boxShadow: '0 0 0 3px rgba(99,102,241,.10)', background: '#fafbff' }
                : {}">
              <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:12px;">
                <div style="flex:1; min-width:0;">

                  <div style="display:flex; align-items:baseline; gap:8px; flex-wrap:wrap; margin-bottom:10px;">
                    <span style="font-weight:700; font-size:15px; color:var(--gray-800);">{{ v.marca }}</span>
                    <span style="font-size:14px; color:var(--gray-600);">{{ v.modelo }}</span>
                    <span
                      style="font-size:12px; color:var(--gray-400); background:var(--gray-100); padding:2px 7px; border-radius:20px;">{{
                        v.ano }}</span>
                  </div>

                  <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                    <span class="badge badge-success" style="font-size:12px; letter-spacing:.6px; padding:3px 10px;">{{
                      v.placa }}</span>
                    <div style="display:flex; align-items:center; gap:6px;">
                      <span v-if="v.cor"
                        :style="{ background: v.cor.startsWith('#') ? v.cor : '#ccc', border: v.cor === '#FFFFFF' ? '1px solid #d1d5db' : 'none' }"
                        style="width:13px; height:13px; border-radius:50%; flex-shrink:0; box-shadow:0 1px 2px rgba(0,0,0,.15);">
                      </span>
                      <span style="font-size:12px; color:var(--gray-500);">{{ nomeDaCor(v.cor) }}</span>
                    </div>
                  </div>

                </div>

                <div style="display:flex; gap:6px; flex-shrink:0; padding-top:2px;">
                  <button class="btn-icone" title="Revisões" style="font-size:15px;"
                    @click="abrirGerenciadorRevisoesNoModal(v)">🔧</button>
                  <button class="btn-icone" title="Editar" style="font-size:15px;"
                    @click="editarVeiculoNaLista(v)">✏️</button>
                  <button class="btn-icone btn-icone-perigo" title="Excluir" style="font-size:15px;"
                    @click="confirmarExclusaoVeiculo(v)">🗑️</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div
          style="padding:32px 32px 32px 32px; overflow-y:auto; max-height:80vh; background:#f8f9fb; display:flex; flex-direction:column; gap:0;">

          <div
            style="display:flex; align-items:center; justify-content:space-between; margin-bottom:24px; padding-right: 20px;">
            <div>
              <p style="margin:0; font-size:16px; font-weight:700; color:var(--gray-800);">
                {{ formVeiculo.id ? 'Editar veículo' : 'Novo veículo' }}
              </p>
              <p style="margin:3px 0 0; font-size:12px; color:var(--gray-500);">
                {{ formVeiculo.id ? 'Altere os dados e salve' : 'Preencha os dados do veículo' }}
              </p>
            </div>
          </div>

          <div style="display:flex; flex-direction:column; gap:18px; flex:1;">

            <div style="display:flex; flex-direction:column; gap:6px;">
              <label
                style="font-size:12px; font-weight:600; color:var(--gray-600); text-transform:uppercase; letter-spacing:.5px;">Marca</label>
              <input v-if="formVeiculo.id" :value="formVeiculo.marca" readonly
                style="padding:10px 14px; border:1.5px solid var(--gray-200); border-radius:8px; background:var(--gray-100); color:var(--gray-500); cursor:not-allowed; font-size:14px;" />
              <select v-else v-model="marcaSelecionadaCodigo" :class="{ 'input-erro': errosVeiculo.marca }"
                style="padding:10px 14px; border:1.5px solid var(--gray-200); border-radius:8px; font-size:14px; background:#fff; outline:none; cursor:pointer;"
                @change="aoMudarMarca(false); delete errosVeiculo.marca" :disabled="carregandoMarcas">
                <option value="">{{ carregandoMarcas ? 'Buscando na FIPE...' : 'Selecione a marca...' }}</option>
                <option v-for="m in marcasFipe" :key="m.codigo" :value="m.codigo">{{ m.nome }}</option>
              </select>
              <span class="msg-erro" v-if="errosVeiculo.marca">{{ errosVeiculo.marca }}</span>
            </div>

            <div style="display:flex; flex-direction:column; gap:6px;">
              <label
                style="font-size:12px; font-weight:600; color:var(--gray-600); text-transform:uppercase; letter-spacing:.5px;">Modelo</label>
              <input v-if="formVeiculo.id" :value="formVeiculo.modelo" readonly
                style="padding:10px 14px; border:1.5px solid var(--gray-200); border-radius:8px; background:var(--gray-100); color:var(--gray-500); cursor:not-allowed; font-size:14px;" />
              <select v-else v-model="formVeiculo.modelo" :class="{ 'input-erro': errosVeiculo.modelo }"
                style="padding:10px 14px; border:1.5px solid var(--gray-200); border-radius:8px; font-size:14px; background:#fff; outline:none; cursor:pointer;"
                @change="delete errosVeiculo.modelo" :disabled="!marcaSelecionadaCodigo || carregandoModelos">
                <option value="">
                  {{ carregandoModelos ? 'Buscando modelos...' : (marcaSelecionadaCodigo ? 'Selecione o modelo...' :
                    'Selecione a marca primeiro') }}
                </option>
                <option v-for="mod in modelosFipe" :key="mod.codigo" :value="mod.nome">{{ mod.nome }}</option>
              </select>
              <span class="msg-erro" v-if="errosVeiculo.modelo">{{ errosVeiculo.modelo }}</span>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
              <div style="display:flex; flex-direction:column; gap:6px;">
                <label
                  style="font-size:12px; font-weight:600; color:var(--gray-600); text-transform:uppercase; letter-spacing:.5px;">Ano</label>
                <input v-if="formVeiculo.id" :value="formVeiculo.ano" readonly
                  style="padding:10px 14px; border:1.5px solid var(--gray-200); border-radius:8px; background:var(--gray-100); color:var(--gray-500); cursor:not-allowed; font-size:14px;" />
                <input v-else v-model="formVeiculo.ano" type="number" placeholder="2024" min="1900"
                  :max="anoMaximoVeiculo" :class="{ 'input-erro': errosVeiculo.ano }"
                  style="padding:10px 14px; border:1.5px solid var(--gray-200); border-radius:8px; font-size:14px; outline:none; background:#fff;"
                  @input="delete errosVeiculo.ano" />
                <span class="msg-erro" v-if="errosVeiculo.ano">{{ errosVeiculo.ano }}</span>
              </div>
              <div style="display:flex; flex-direction:column; gap:6px;">
                <label
                  style="font-size:12px; font-weight:600; color:var(--gray-600); text-transform:uppercase; letter-spacing:.5px;">Placa</label>
                <input v-model="formVeiculo.placa" placeholder="ABC1D23" :class="{ 'input-erro': errosVeiculo.placa }"
                  style="padding:10px 14px; border:1.5px solid var(--gray-200); border-radius:8px; font-size:14px; outline:none; background:#fff; text-transform:uppercase; font-weight:600; letter-spacing:1px;"
                  @input="formVeiculo.placa = formVeiculo.placa.toUpperCase(); delete errosVeiculo.placa"
                  maxlength="8" />
                <span class="msg-erro" v-if="errosVeiculo.placa">{{ errosVeiculo.placa }}</span>
              </div>
            </div>

            <div style="display:flex; flex-direction:column; gap:8px;">
              <label
                style="font-size:12px; font-weight:600; color:var(--gray-600); text-transform:uppercase; letter-spacing:.5px;">Cor</label>

              <div
                style="display:flex; flex-wrap:wrap; gap:9px; padding:14px; background:#fff; border:1.5px solid var(--gray-200); border-radius:8px;">
                <button v-for="c in todasAsCores" :key="c.valor" type="button" :title="c.nome"
                  @click="selecionarCorVeiculo(c.valor)" :style="{
                    width: '30px', height: '30px', borderRadius: '50%',
                    background: c.valor,
                    border: formVeiculo.cor === c.valor ? '3px solid var(--primary)' : '2px solid #d1d5db',
                    cursor: 'pointer', flexShrink: 0, outline: 'none',
                    boxShadow: c.valor === '#FFFFFF' ? 'inset 0 0 0 1px #e5e7eb' : '0 1px 3px rgba(0,0,0,.15)',
                    transform: formVeiculo.cor === c.valor ? 'scale(1.15)' : 'scale(1)',
                    transition: 'transform .12s, border .12s'
                  }">
                </button>

                <label title="Cor personalizada" style="width:30px; height:30px; border-radius:50%; border:2px dashed #9ca3af; cursor:pointer;
                         display:flex; align-items:center; justify-content:center; font-size:16px; font-weight:600;
                         flex-shrink:0; background:#fff; color:#9ca3af; position:relative; user-select:none;
                         transition:border-color .12s;"
                  @mouseenter="$event.target.style.borderColor = 'var(--primary)'"
                  @mouseleave="$event.target.style.borderColor = '#9ca3af'">
                  +
                  <input type="color" v-model="corCustomTemp" style="opacity:0; width:0; height:0; position:absolute;"
                    @change="abrirNomeCorCustom" />
                </label>
              </div>

              <div
                style="display:flex; align-items:center; gap:8px; padding:8px 12px; background:#fff; border:1px solid var(--gray-100); border-radius:8px;">
                <span
                  :style="{ background: formVeiculo.cor || '#e5e7eb', border: formVeiculo.cor === '#FFFFFF' ? '1px solid #d1d5db' : 'none' }"
                  style="width:18px; height:18px; border-radius:50%; flex-shrink:0; box-shadow:0 1px 3px rgba(0,0,0,.15);"></span>
                <span style="font-size:13px; color:var(--gray-700); font-weight:500;">
                  {{ nomeDaCor(formVeiculo.cor) || 'Nenhuma cor selecionada' }}
                </span>
              </div>

              <div v-if="nomeandoCorCustom"
                style="background:#fff; border:1.5px solid var(--primary); border-radius:10px; padding:16px;">
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

              <span class="msg-erro" v-if="errosVeiculo.cor">{{ errosVeiculo.cor }}</span>
            </div>

          </div>

          <div style="display:flex; gap:10px; margin-top:28px; padding-top:20px; border-top:1px solid var(--gray-100);">
            <button class="btn btn-ghost" style="flex:1; padding:11px; font-size:14px;" @click="cancelarEdicaoVeiculo">
              Cancelar
            </button>
            <button class="btn btn-primary" style="flex:2; padding:11px; font-size:14px; font-weight:600;"
              @click="salvarVeiculo" :disabled="salvandoVeiculo">
              {{ salvandoVeiculo ? 'Salvando...' : (formVeiculo.id ? 'Salvar alterações' : 'Adicionar veículo') }}
            </button>
          </div>

        </div>
      </div>

    </div>
  </div>


  <ModalRevisao v-if="modalRevisoesAberto && veiculoAtual" :veiculo="veiculoAtual"
    @fechar="fecharGerenciadorRevisoes" />

</template>


<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { pessoasAPI, veiculosAPI, api } from '../services/api'
import ModalRevisao from '../components/ModalRevisao.vue'


// ── ESTADO DA TELA ────────────────────────────────────────────────────────────

const pessoas = ref([])
const carregando = ref(true)
const modalAberto = ref(false)
const editando = ref(null)
const salvando = ref(false)
const erros = ref({})
const busca = ref('')
const totalPessoas = ref(0)
const proximaPagina = ref(null)
const paginaAnterior = ref(null)
const paginaAtual = ref(1)
const limitePaginacao = ref(10)
const buscandoCEP = ref(false)
const cepEncontrado = ref(false)

// Limites de data
const dataMaximaNascimento = computed(() => new Date().toISOString().split('T')[0])
const anoMaximoVeiculo = computed(() => new Date().getFullYear() + 1)


// ── PAGINAÇÃO ─────────────────────────────────────────────────────────────────

const inicioPaginacao = computed(() => {
  if (totalPessoas.value === 0) return 0
  return (paginaAtual.value - 1) * limitePaginacao.value + 1
})
const fimPaginacao = computed(() =>
  Math.min(paginaAtual.value * limitePaginacao.value, totalPessoas.value)
)


// ── EXCLUSÃO DE PESSOA ────────────────────────────────────────────────────────

const modalExclusaoAberto = ref(false)
const pessoaParaExcluir = ref(null)
const excluindo = ref(false)

function confirmarExclusao(pessoa) {
  pessoaParaExcluir.value = pessoa
  modalExclusaoAberto.value = true
}

async function deletar() {
  excluindo.value = true
  await pessoasAPI.deletar(pessoaParaExcluir.value.id)
  modalExclusaoAberto.value = false
  pessoaParaExcluir.value = null
  excluindo.value = false
  await carregar()
}


// ── FORMULÁRIO DE PESSOA ──────────────────────────────────────────────────────

const formVazio = () => ({
  nome: '', cpf: '', email: '', telefone: '',
  data_nascimento: '', sexo: '',
  cep: '', rua: '', bairro: '', numero: '', cidade: '', estado: ''
})
const form = ref(formVazio())


// ── VIACEP ────────────────────────────────────────────────────────────────────

async function buscarCEP() {
  const cepLimpo = form.value.cep.replace(/\D/g, '')
  if (cepLimpo.length !== 8) return
  buscandoCEP.value = true
  cepEncontrado.value = false
  try {
    const res = await fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`)
    const data = await res.json()
    if (data.erro) { erros.value.cep = 'CEP não encontrado'; return }
    form.value.rua = data.logradouro || ''
    form.value.bairro = data.bairro || ''
    form.value.cidade = data.localidade || ''
    form.value.estado = data.uf || ''
    cepEncontrado.value = true
    setTimeout(() => {
      document.querySelector('input[placeholder="Ex: 123 ou S/N"]')?.focus()
    }, 50)
  } catch {
    erros.value.cep = 'Não foi possível consultar o CEP. Preencha o endereço manualmente.'
  } finally {
    buscandoCEP.value = false
  }
}


// ── CORES ─────────────────────────────────────────────────────────────────────

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
  formVeiculo.value.cor = valor
  delete errosVeiculo.value.cor
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


// ── MODAL DE VEÍCULOS ─────────────────────────────────────────────────────────

const modalVeiculoNovoAberto = ref(false)
const pessoaSelecionada = ref(null)
const veiculosDaPessoa = ref([])
const carregandoVeiculos = ref(false)
const salvandoVeiculo = ref(false)
const errosVeiculo = ref({})
const veiculoParaExcluir = ref(null)
const modalExclusaoVeiculoAberto = ref(false)
const excluindoVeiculo = ref(false)

const marcasFipe = ref([])
const modelosFipe = ref([])
const carregandoMarcas = ref(false)
const carregandoModelos = ref(false)
const marcaSelecionadaCodigo = ref('')

const formVeiculoVazio = () => ({
  proprietario: null, marca: '', modelo: '', ano: '', placa: '', cor: ''
})
const formVeiculo = ref(formVeiculoVazio())

async function carregarMarcasFipe() {
  carregandoMarcas.value = true
  try {
    const res = await axios.get('https://parallelum.com.br/fipe/api/v1/carros/marcas')
    marcasFipe.value = res.data
  } catch (e) { console.error('Erro ao buscar marcas da FIPE', e) }
  carregandoMarcas.value = false
}

async function aoMudarMarca(isEdit = false) {
  const marcaObj = marcasFipe.value.find(m => String(m.codigo) === String(marcaSelecionadaCodigo.value))
  if (!isEdit) {
    formVeiculo.value.marca = marcaObj ? marcaObj.nome : ''
    formVeiculo.value.modelo = ''
  }
  modelosFipe.value = []
  if (!marcaSelecionadaCodigo.value) return
  carregandoModelos.value = true
  try {
    const res = await axios.get(`https://parallelum.com.br/fipe/api/v1/carros/marcas/${marcaSelecionadaCodigo.value}/modelos`)
    modelosFipe.value = res.data.modelos
  } catch (e) { console.error('Erro ao buscar modelos da FIPE', e) }
  carregandoModelos.value = false
}

async function abrirModalVeiculo(pessoa) {
  pessoaSelecionada.value = pessoa
  formVeiculo.value = formVeiculoVazio()
  formVeiculo.value.proprietario = pessoa.id
  errosVeiculo.value = {}
  marcaSelecionadaCodigo.value = ''
  modelosFipe.value = []
  nomeandoCorCustom.value = false
  modalVeiculoNovoAberto.value = true

  carregandoVeiculos.value = true
  try {
    const res = await veiculosAPI.listar('', pessoa.id)
    veiculosDaPessoa.value = res.data.results || res.data
  } catch (e) { console.error(e) }
  carregandoVeiculos.value = false
}

function fecharModalVeiculo() {
  modalVeiculoNovoAberto.value = false
  formVeiculo.value = formVeiculoVazio()
  errosVeiculo.value = {}
  marcaSelecionadaCodigo.value = ''
  modelosFipe.value = []
  nomeandoCorCustom.value = false
}

// Cancela edição e volta para "novo veículo" SEM fechar o modal
function cancelarEdicaoVeiculo() {
  formVeiculo.value = formVeiculoVazio()
  formVeiculo.value.proprietario = pessoaSelecionada.value?.id ?? null
  errosVeiculo.value = {}
  marcaSelecionadaCodigo.value = ''
  modelosFipe.value = []
  nomeandoCorCustom.value = false
}

function editarVeiculoNaLista(veiculo) {
  formVeiculo.value = { ...veiculo }
  errosVeiculo.value = {}
  nomeandoCorCustom.value = false

  const encontrada = veiculo?.marca
    ? marcasFipe.value.find(m => m.nome.toLowerCase() === veiculo.marca.toLowerCase())
    : null

  marcaSelecionadaCodigo.value = encontrada ? encontrada.codigo : ''
  if (encontrada) aoMudarMarca(true)
  else modelosFipe.value = []
}

function confirmarExclusaoVeiculo(veiculo) {
  veiculoParaExcluir.value = veiculo
  modalExclusaoVeiculoAberto.value = true
}

async function deletarVeiculo() {
  excluindoVeiculo.value = true
  await veiculosAPI.deletar(veiculoParaExcluir.value.id)
  modalExclusaoVeiculoAberto.value = false
  veiculoParaExcluir.value = null
  excluindoVeiculo.value = false
  const res = await veiculosAPI.listar('', pessoaSelecionada.value.id)
  veiculosDaPessoa.value = res.data.results || res.data
}

function validarVeiculo() {
  errosVeiculo.value = {}
  if (!formVeiculo.value.id && !marcaSelecionadaCodigo.value)
    errosVeiculo.value.marca = 'Marca obrigatória'
  if (!formVeiculo.value.modelo)
    errosVeiculo.value.modelo = 'Modelo obrigatório'
  if (!formVeiculo.value.ano)
    errosVeiculo.value.ano = 'Ano obrigatório'
  else if (formVeiculo.value.ano < 1900 || formVeiculo.value.ano > anoMaximoVeiculo.value)
    errosVeiculo.value.ano = `Ano inválido (1900 – ${anoMaximoVeiculo.value})`
  if (!formVeiculo.value.placa)
    errosVeiculo.value.placa = 'Placa obrigatória'
  else if (!/^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$|^[A-Z]{3}-[0-9]{4}$/.test(formVeiculo.value.placa.toUpperCase()))
    errosVeiculo.value.placa = 'Placa inválida (ex: ABC1D23)'
  if (!formVeiculo.value.cor || formVeiculo.value.cor.length < 2)
    errosVeiculo.value.cor = 'Cor obrigatória'
  return Object.keys(errosVeiculo.value).length === 0
}

async function salvarVeiculo() {
  if (!validarVeiculo()) return
  salvandoVeiculo.value = true
  try {
    if (formVeiculo.value.id) {
      await veiculosAPI.atualizar(formVeiculo.value.id, formVeiculo.value)
    } else {
      await veiculosAPI.criar(formVeiculo.value)
    }
    // Volta para "novo veículo" sem fechar o modal
    cancelarEdicaoVeiculo()
    const res = await veiculosAPI.listar('', pessoaSelecionada.value.id)
    veiculosDaPessoa.value = res.data.results || res.data
  } catch (e) {
    if (e.response?.data?.placa) errosVeiculo.value.placa = e.response.data.placa[0]
  }
  salvandoVeiculo.value = false
}


// ── GERENCIADOR DE REVISÕES ───────────────────────────────────────────────────

const modalRevisoesAberto = ref(false)
const veiculoAtual = ref(null)

function abrirGerenciadorRevisoesNoModal(veiculo) {
  veiculoAtual.value = veiculo
  modalRevisoesAberto.value = true
}

function fecharGerenciadorRevisoes() {
  modalRevisoesAberto.value = false
  veiculoAtual.value = null
}


// ── BUSCA COM DEBOUNCE ────────────────────────────────────────────────────────

let buscaTimeout = null
watch(busca, (termo) => {
  clearTimeout(buscaTimeout)
  buscaTimeout = setTimeout(() => carregar(null, termo), 400)
})


// ── FORMATADORES ──────────────────────────────────────────────────────────────

function formatarCPF(valor) {
  const limpo = valor.replace(/\D/g, '').slice(0, 11)
  return limpo
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d{1,2})$/, '$1-$2')
}

function formatarTelefone(valor) {
  const limpo = valor.replace(/\D/g, '').slice(0, 11)
  if (limpo.length <= 10)
    return limpo.replace(/(\d{2})(\d)/, '($1) $2').replace(/(\d{4})(\d)/, '$1-$2')
  return limpo.replace(/(\d{2})(\d)/, '($1) $2').replace(/(\d{5})(\d)/, '$1-$2')
}

function formatarCEP(valor) {
  const limpo = valor.replace(/\D/g, '').slice(0, 8)
  return limpo.replace(/(\d{5})(\d)/, '$1-$2')
}

function formatarData(data) {
  if (!data) return '—'
  const [y, m, d] = data.split('-')
  return `${d}/${m}/${y}`
}

function validarCPF(cpf) {
  const limpo = cpf.replace(/\D/g, '')
  if (limpo.length !== 11 || /^(\d)\1+$/.test(limpo)) return false
  let soma = 0
  for (let i = 0; i < 9; i++) soma += parseInt(limpo[i]) * (10 - i)
  let resto = (soma * 10) % 11
  if (resto === 10 || resto === 11) resto = 0
  if (resto !== parseInt(limpo[9])) return false
  soma = 0
  for (let i = 0; i < 10; i++) soma += parseInt(limpo[i]) * (11 - i)
  resto = (soma * 10) % 11
  if (resto === 10 || resto === 11) resto = 0
  return resto === parseInt(limpo[10])
}


// ── VALIDAÇÃO DE PESSOA ───────────────────────────────────────────────────────

function validarForm() {
  erros.value = {}
  if (!form.value.nome || form.value.nome.length < 3)
    erros.value.nome = 'Nome deve ter pelo menos 3 caracteres'
  if (!form.value.email || !form.value.email.includes('@'))
    erros.value.email = 'Email inválido'
  if (!form.value.cpf)
    erros.value.cpf = 'CPF é obrigatório'
  else if (!validarCPF(form.value.cpf))
    erros.value.cpf = 'CPF inválido'
  if (!form.value.telefone)
    erros.value.telefone = 'Telefone é obrigatório'
  else if (form.value.telefone.replace(/\D/g, '').length < 10)
    erros.value.telefone = 'Telefone inválido (mínimo 10 dígitos)'
  if (!form.value.data_nascimento) {
    erros.value.data_nascimento = 'Data de nascimento é obrigatória'
  } else {
    const hoje = new Date(); hoje.setHours(0, 0, 0, 0)
    const nasc = new Date(form.value.data_nascimento + 'T00:00:00')
    if (nasc > hoje)
      erros.value.data_nascimento = 'Data não pode ser no futuro'
    else if (nasc.getFullYear() < 1900)
      erros.value.data_nascimento = 'Ano inválido (mínimo 1900)'
  }
  if (!form.value.sexo)
    erros.value.sexo = 'Selecione o sexo'
  if (!form.value.cep)
    erros.value.cep = 'CEP é obrigatório'
  else if (form.value.cep.replace(/\D/g, '').length !== 8)
    erros.value.cep = 'CEP deve conter exatamente 8 dígitos'
  if (!form.value.rua)
    erros.value.rua = 'Rua é obrigatória'
  return Object.keys(erros.value).length === 0
}


// ── CRUD E PAGINAÇÃO ──────────────────────────────────────────────────────────

async function carregar(url = null, search = '') {
  carregando.value = true
  try {
    const res = url ? await api.get(url) : await pessoasAPI.listar(search)
    pessoas.value = res.data.results || res.data
    totalPessoas.value = res.data.count || res.data.length
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

    if (pessoas.value.length > 0 && url === null)
      limitePaginacao.value = pessoas.value.length
  } catch (e) { console.error('Erro ao carregar pessoas', e) }
  finally { carregando.value = false }
}

function abrirModal(pessoa = null) {
  editando.value = pessoa
  form.value = pessoa ? { ...formVazio(), ...pessoa } : formVazio()
  erros.value = {}
  cepEncontrado.value = !!pessoa?.rua
  modalAberto.value = true
}

function fecharModal() {
  modalAberto.value = false
  editando.value = null
  form.value = formVazio()
  erros.value = {}
  cepEncontrado.value = false
}

async function salvar() {
  if (!validarForm()) return
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
    if (e.response?.data) {
      const ed = e.response.data
      if (ed.cpf) erros.value.cpf = ed.cpf[0]
      if (ed.email) erros.value.email = ed.email[0]
      if (ed.nome) erros.value.nome = ed.nome[0]
      if (ed.cep) erros.value.cep = ed.cep[0]
    }
  }
  salvando.value = false
}


// ── CICLO DE VIDA ─────────────────────────────────────────────────────────────

onMounted(async () => {
  carregarCoresCustomizadas()
  await carregarMarcasFipe()
  await carregar()
})
</script>