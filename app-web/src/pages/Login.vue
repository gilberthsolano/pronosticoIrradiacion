<template>
  <h1 style="text-align: center; margin-bottom: 20px;">Iniciar sesión</h1>
  <form
    @submit.prevent="procesarFormulario">
    <div>
      <label>Usuario: </label>
      <input 
        type="text" 
        v-model="campos.usuario"
        required>
    </div>
    <div>
      <label>Contraseña: </label>
      <input 
        type="password" 
        v-model="campos.clave"
        required  >
    </div>
    <button
      type="submit"
      :disabled="cargando">Ingresar</button>
  </form>
  <footer style="margin-top: 30px;margin-bottom: 10px;">
    <a @click="globalStore.cambiarPagina('HOME')">Regresar</a>
  </footer>
</template>

<script setup lang="ts">
import { useGlobalStore } from "@/stores/global";
import {reactive, ref} from "vue";

const globalStore = useGlobalStore()
const API = "http://localhost:8000"
const campos = reactive({
  usuario: '',
  clave: ''
})
const cargando = ref(false);

const procesarFormulario = async()=>{
  try {
    cargando.value = true;
    globalStore.autenticarUsuario(campos)
  } catch (error) {
    console.log(error);    
  }finally{
    cargando.value = false;
  }
}
</script>

<style scoped>
header {
  line-height: 1.5;
}

form{
  width: 300px;
}

form label{
  display: block;
  margin-bottom: 5px;
}
form input{
  display: block;
  width: 100%;
  padding: 5px;
  border-radius: 10px;
  border-color: transparent;
  margin-bottom: 10px;
}

form button{
  display: block;
  width: 100%;
  padding: 8px;
  border-radius: 15px;
  margin-top: 20px;
  font-size: 20px;
}

.resultado{
  margin-top: 15px;
  font-size: 24px;
}

form{
  margin-left: auto;
  margin-right: auto;
}
</style>
