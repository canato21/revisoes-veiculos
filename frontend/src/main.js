/**
 * Este é o primeiro arquivo JavaScript executado quando o sistema abre.
 * Ele cria a aplicação Vue, registra os plugins e a monta no HTML.
 */

import { createApp } from 'vue'   // função para criar a aplicação Vue
import App from './App.vue'        // componente raiz (layout principal com topbar)
import router from './router'      // sistema de navegação entre telas
import './style.css'               // estilos globais (CSS aplicado em toda a app)

/**
 * createApp(App): cria a instância da aplicação Vue usando App.vue como raiz
 * .use(router): registra o Vue Router (habilita RouterLink e RouterView)
 * .mount('#app'): conecta a aplicação ao elemento <div id="app"> do index.html
 *
 * Após o mount, o Vue assume o controle do #app e renderiza os componentes.
 */
createApp(App).use(router).mount('#app')
