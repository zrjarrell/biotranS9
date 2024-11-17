from fastapi import FastAPI
from databases import Database

import sqlalchemy
from sqlalchemy.sql import select

metadata = sqlalchemy.MetaData()

chemical = sqlalchemy.Table(
    "chemical",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("pubchemid", sqlalchemy.Text, nullable=False, unique=True),
    sqlalchemy.Column("smiles", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("formula", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("monoisotopic", sqlalchemy.Float, nullable=False),
)

database = Database("sqlite:///biotransdb.db")

app = FastAPI()

@app.get("/chemicals/")
async def fetch_data(name: str):
    print(name)
    query = f"SELECT * FROM chemical WHERE LOWER(chemical.name) LIKE lower('{name}')"
    print(query)
    results = await database.fetch_all(query=query)
    return results

#f'SELECT * FROM precursor LEFT JOIN metabolite ON precursor.id = metabolite.precursorId LEFT JOIN enzyme ON metabolite.id = enzyme.metaboliteId WHERE precursor.name = "{drugtable.iloc[i,0]}"'

@app.get("/chemicals_byid/")
async def fetch_data(id: int):
    query = f"SELECT * FROM chemical WHERE id = {str(id)}"
    results = await database.fetch_all(query=query)
    return results

@app.get("/test/")
async def fetch_data(name: str):
    query = select(chemical).where(chemical.c.name.ilike('%' + name + '%'))
    results = await database.fetch_all(query=query)
    return results
