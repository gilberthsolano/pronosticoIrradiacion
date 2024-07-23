import { ref } from 'vue'
import { defineStore } from 'pinia'

const API = "http://localhost:8000"

interface IState{
  pagina: 'HOME' | 'LOGIN' | 'PRONOSTICOS',
}

export const useGlobalStore = defineStore('global',{
  state:():IState=>({
    pagina: 'HOME',
  }),
  actions:{
    autenticarUsuario(campos:{usuario:string,clave:string}){
      if(campos.usuario == "admin" && campos.clave == "admin"){
        this.pagina = 'PRONOSTICOS'
      }else{
        alert("Credenciales incorrectas!")
        return;
      }
    },
    cambiarPagina(pagina: 'HOME' | 'LOGIN'){
      this.pagina = pagina
    }
  }
})
