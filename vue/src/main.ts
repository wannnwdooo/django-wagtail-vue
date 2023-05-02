import { createApp } from 'vue'
import Toast, { POSITION } from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import { registerAllComponents, registerAllDirectives, registerAllPages } from './config/config'
import router from './router'

const app = createApp({
  delimiters: ['${', '}'],
  runtimeCompiler: true
})

registerAllComponents(app)
registerAllPages(app)
registerAllDirectives(app)

app.use(Toast, { position: POSITION.BOTTOM_RIGHT, timeout: 3000 }).use(router)
// app.use(router)
app.mount('#app')

console.log('vue initialized')
