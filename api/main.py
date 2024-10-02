from fastapi import FastAPI
import pymongo
import os

mongo_uri = os.getenv('MONGO_URI')

app = FastAPI()
client = pymongo.MongoClient(mongo_uri)
db = client["gastospublicos"]
per_page = 50

def paginate(collection, offset):
    result = db[collection].find({ }, { "_id": 0 }).skip(offset).limit(per_page)
    return list(result)

def skip(page):
    return (int(page) - 1) * per_page

@app.get("/api/v1/gastos_publicos")
async def gastos_publicos(page = 1):
    return paginate("despesas", skip(page))

@app.get("/api/v1/emendas")
async def emendas_parlamentares(page = 1):
    return paginate("EmendasParlamentares", skip(page))

@app.get("/api/v1/notas_fiscais")
async def notas_fiscais(page = 1):
    return paginate("notasfiscais", skip(page))

@app.get("/api/v1/orcamento")
async def orcamento(page = 1):
    return paginate("orcamento", skip(page))
