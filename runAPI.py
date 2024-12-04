from fastapi import FastAPI
from databases import Database
from sqlalchemy.sql import select
from fastapi.middleware.cors import CORSMiddleware

from tables import chemical, metabolite, enzyme, mass

database = Database("sqlite:///biotransdb.db")

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Welcome to BiotranS9 Explorer!"}

@app.get("/chemicals/")
async def fetch_data(name: str):
    query = select(chemical).where(chemical.c.name.ilike('%' + name + '%'))
    print(query)
    results = await database.fetch_all(query=query)
    return results

@app.get("/chemicals/metabolites/")
async def fetch_data(id: int):
    query = select(chemical, metabolite, enzyme).where(chemical.c.id == metabolite.c.chemicalId).where(metabolite.c.id == enzyme.c.metaboliteId).where(chemical.c.id == id)
    results = await database.fetch_all(query=query)
    return results

@app.get("/test/")
async def fetch_data(id: int):
    query = select(chemical, metabolite, mass).where(chemical.c.id == id).where(chemical.c.id == metabolite.c.chemicalId)
    query = query.outerjoin(mass)
    results = await database.fetch_all(query=query)
    print(query)
    summary = {'tot.predicted': set(), 'detected.metabolites': set(), 'unique.feats.match': set()}
    for result in results:
        summary['tot.predicted'].add(result['id_1'])
        if result['detected']:
            summary['detected.metabolites'].add(result['id_1'])
        if result['id_2']:
            summary['unique.feats.match'].add(str(result['mz']) + "_" + str(result['rt']))
    return summary