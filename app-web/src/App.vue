<template>
  <Pronosticos v-if="pagina == 'PRONOSTICOS'"/>
  <Home v-else-if="pagina == 'HOME'"/>
  <Login v-else-if="pagina == 'LOGIN'"/>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import Home from "./pages/Home.vue";
import Pronosticos from "./pages/Pronosticos.vue";
import { useGlobalStore } from "./stores/global";
import Login from "./pages/Login.vue";

const {pagina} = storeToRefs(useGlobalStore())

</script>

<style scoped>

</style>
