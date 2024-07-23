<template>
  <h1 
    style="text-align: center; margin-bottom: 20px; margin-top: 30px;">
    Listado de pronósticos
  </h1>
  <a @click="globalStore.cambiarPagina('HOME')">Regresar</a>
  <form @submit.prevent="filtrarDatos">
    <label>Inicio:</label>
    <input v-model="filtro.inicio" class="form-control" type="date" required>
    <label>Fin:</label>
    <input v-model="filtro.fin" class="form-control" type="date" required>
    <button type="submit">Filtrar</button>
    <button 
      v-if="pronosticos.length != pronosticosFiltrados.length"
      @click="resetear()">Restaurar ❌</button>
  </form>
  <button 
    v-if="pronosticosFiltrados.length > 0"
    style="margin-bottom: 10px;"
    @click="imprimirPDF()">Rerpote en pdf 🧾</button>
  <table>
    <thead>
      <tr>
        <th>Datos de entrada</th>
        <th>Algoritmo</th>
        <th>Fecha registro</th>
        <th>Irradiación</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="i in pronosticosFiltrados">
        <td>
          {{i.datos_entrada.hora}}h{{ i.datos_entrada.minuto }} - {{ i.datos_entrada.temperatura }} C° 
        </td>
        <td>
          {{ i.modelo }}
        </td>
        <td>
          {{ new Date(i.fecha).toLocaleDateString() }}
        </td>
        <td>
          {{ i.irradiacion }} W/m²
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import { useGlobalStore } from "@/stores/global";
import {onBeforeMount, reactive, ref} from "vue";
import moment from "moment";
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

interface IPronostico{
  datos_entrada:{
    hora:number
    minuto: number
    temperatura: number
  },
  fecha: string
  modelo: string
  irradiacion: number
}

const globalStore = useGlobalStore()
const API = "http://localhost:8000"
const pronosticos = ref<IPronostico[]>([])
const pronosticosFiltrados = ref<IPronostico[]>([])
const filtro = reactive({
  inicio: '',
  fin: ''
})

const resetear = ()=>{
  pronosticosFiltrados.value = [...pronosticos.value]
  filtro.inicio = '';
  filtro.fin = '';
}

const filtrarDatos = ()=>{
  pronosticosFiltrados.value = pronosticos.value.filter(x => 
    moment(x.fecha).isSameOrAfter(moment(filtro.inicio)) && 
    moment(x.fecha).isSameOrBefore(moment(filtro.fin))
  )
}

const imprimirPDF = ()=>{
  const doc = new jsPDF()
  autoTable(doc, {
    head: [['Datos entrada','Algoritmo','Fecha de registro','Irradiación']],
    body: pronosticosFiltrados.value.map(x => [
      `${x.datos_entrada.hora}h${x.datos_entrada.minuto} - ${x.datos_entrada.temperatura} C°`,
      x.modelo,
      moment(x.fecha).format('DD/MM/YYYY'),
      `${x.irradiacion} W/m²`
    ])
  })
  doc.save('reporte')
}

onBeforeMount(async()=>{
  const data = await(await fetch(`${API}/api/pronosticos`)).json()
  pronosticos.value = data.pronosticos;
  pronosticosFiltrados.value = data.pronosticos;
})
</script>

<style scoped>
table{
  border: 1px solid;
  width: 600px;
  margin-bottom: 30px;
}
th{
  font-weight: bold;
  border: 1px solid;
}
td{
  border: 1px solid;
  text-align: center;
}

form{
  display: flex;
  width: 600px;
  margin-top: 10px;
}

form label{
  margin-right: 5px;
}
form input{
  width: 120px;
  padding: 5px;
  border-radius: 10px;
  border-color: transparent;
  margin-bottom: 10px;
  margin-right: 10px;
}

button{
  border-radius: 15px;
  font-size: 18px;
  height: 35px;
  cursor: pointer;
  margin-right: 10px;
}

</style>