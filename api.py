from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from pymongo import MongoClient
import datetime

client = MongoClient('mongodb+srv://admin:admin@cluster0.9p5wrdm.mongodb.net/db_universidad_loja?retryWrites=true&w=majority')
db = client['irradicacion_db']

class DatosEntrada(BaseModel):
  temperatura: float
  hora: int
  minuto: int

class DatosLogin(BaseModel):
  usuario: str
  clave: str

# Cargar el modelos
modelo_rl_modulo = joblib.load('modelo_regresion_lineal_modulo.joblib')
modelo_rl_irradiacion = joblib.load('modelo_regresion_lineal_irradiacion.joblib')
modelo_rna = load_model('modelo_rna_v3')
app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.post("/api/pronostico-irradiacion")
def pronostico_irradiacion(body: DatosEntrada):
  temperaturaModulo = modelo_rl_modulo.predict([[body.temperatura, body.hora + (body.minuto / 60)]])[0]
  irradiacion = modelo_rl_irradiacion.predict([[temperaturaModulo, body.temperatura, body.hora + (body.minuto / 60)]])[0]

  db['pronosticos'].insert_one({
    'datos_entrada': {
      'temperatura': body.temperatura,
      'hora': body.hora,
      'minuto': body.minuto
    },
    'modelo': 'regresión lineal',
    'irradiacion': round(irradiacion,2),
    'fecha': datetime.datetime.now()
  })
  return {
    "irradiacion": round(irradiacion,2)
  }

@app.post("/api/pronostico-rna-irradiacion")
def pronostico_rna_irradiacion(body: DatosEntrada):
  irradiacion = modelo_rna.predict([[body.temperatura, body.hora, body.minuto]])[0][0]
  db['pronosticos'].insert_one({
    'datos_entrada': {
      'temperatura': body.temperatura,
      'hora': body.hora,
      'minuto': body.minuto
    },
    'modelo': 'redes neuronales',
    'irradiacion': round(float(irradiacion),2),
    'fecha': datetime.datetime.now()
  })
  proximos = []
  for i in range(4):
    if body.hora < 23:
      body.hora += 1
    else:
      body.hora = 0
    proximos.append({
      'hora':body.hora,
      'minuto': body.minuto,
      'irradiacion': round(float(modelo_rna.predict([[body.temperatura, body.hora, body.minuto]])[0][0]),2)
    })

  return {
    "irradiacion": round(float(irradiacion),2),
    'proximos': proximos  
  }

@app.get('/api/pronosticos')
def pronosticos():
  items = []
  for i in db['pronosticos'].find():
    items.append({
      'datos_entrada': i['datos_entrada'],
      'modelo': i['modelo'],
      'irradiacion': i['irradiacion'],
      'fecha': i['fecha']
    })
  return {
    'pronosticos': items,
  }

@app.post("/api/login")
def pronostico_irradiacion(body: DatosLogin):
  if body.clave != "admin" and body.usuario != "admin":
    raise HTTPException(status_code=400, detail="Credenciales incorrectas!")
  return body