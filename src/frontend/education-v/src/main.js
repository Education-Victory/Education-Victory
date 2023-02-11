import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


import '../node_modules/bulma/css/bulma.css'

import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faArrowLeft, faArrowRight, faUser, faGamepad,faCode, faDiagramProject } from "@fortawesome/free-solid-svg-icons";

library.add(faArrowLeft, faArrowRight,faUser, faGamepad,faCode,faDiagramProject )
const app = createApp(App)

app.component("font-awesome-icon", FontAwesomeIcon)
app.use(router)

app.mount('#app')
