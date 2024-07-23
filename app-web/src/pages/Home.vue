<template>
  <h1 style="text-align: center; margin-bottom: 20px;">Pronóstico de irradiación en Loja</h1>
  <form
    @submit.prevent="procesarFormulario">
    <div>
      <label>Fecha y hora: </label>
      <input 
        type="datetime-local" 
        v-model="campos.fecha"
        required>
    </div>
    <div>
      <label>Temperatura C°: </label>
      <input 
        type="number" 
        min="10" 
        max="80" 
        step="0.1" 
        v-model="campos.temperatura"
        required  >
    </div>
    <button
      type="submit"
      :disabled="cargando">Enviar</button>
  </form>
  <template v-if="!cargando">
    <h3 class="resultado" v-if="irradiacion != null">
      Irradiación (Algoritmo Regresion Lineal): {{ irradiacion }} W/m² <br>
      Irradiación (Algoritmo RNA): {{ irradiacionRNA }} W/m²
    </h3>
    <h3 
      v-if="irradiacion != null"
      style="margin-top: 10px; display: flex;align-items: center;">
      Próximas 4 horas 
        <span style="font-size: 30px;">⛅</span>
      </h3>
    <ul v-for="item in proximasHoras">
      <li>
        <span style="margin-right: 20px;">🕐{{ item.hora }}h{{ item.minuto == 0 ? '00':item.minuto }}</span>
        🌞 {{ item.irradiacion }} W/m²
      </li>
    </ul>
  </template>
  <footer style="margin-top: 30px;margin-bottom: 10px;">
    <a @click="globalStore.cambiarPagina('LOGIN')">Ver todos los pronósticos</a>
  </footer>
</template>

<script setup lang="ts">
import { useGlobalStore } from "@/stores/global";
import {reactive, ref} from "vue";

const globalStore = useGlobalStore()
const API = "http://localhost:8000"
const campos = reactive({
  fecha: '',
  temperatura: 0
})
const irradiacion = ref<number | null>(null);
const irradiacionRNA = ref<number | null>(null);
const cargando = ref(false);
const proximasHoras = ref<{hora:number,minuto:number,irradiacion:number}[]>([])

const pronosticoRegresion = async()=>{
  irradiacion.value = null;
  const fecha = new Date(campos.fecha);
  const respuesta = await fetch(`${API}/api/pronostico-irradiacion`,{
    method: 'POST',
    headers:{
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({hora: fecha.getHours(), minuto: fecha.getMinutes(), temperatura: campos.temperatura})
  });
  const data = await respuesta.json()
  irradiacion.value = data?.irradiacion ?? null;
}

const pronosticoRNA = async()=>{
  irradiacionRNA.value = null;
  const fecha = new Date(campos.fecha);
  const respuesta = await fetch(`${API}/api/pronostico-rna-irradiacion`,{
    method: 'POST',
    headers:{
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({hora: fecha.getHours(), minuto: fecha.getMinutes(), temperatura: campos.temperatura})
  });
  const data = await respuesta.json()
  irradiacionRNA.value = data?.irradiacion ?? null;
  proximasHoras.value = data.proximos ?? []  
}

const procesarFormulario = async()=>{
  try {
    cargando.value = true;
    await pronosticoRegresion()
    await pronosticoRNA()
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
