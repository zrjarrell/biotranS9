from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ChemicalSchema(BaseModel):
    id: int
    pubchemid: str
    smiles: str
    formula: str
    name: str
    monoisotopic: float

    class Config:
        orm_mode = True

class ExperimentSchema(BaseModel):
    id: int
    name: str
    date: date

    class Config:
        orm_mode = True

class MachineSchema(BaseModel):
    id: int
    name: str
    sensitivity: float

    class Config:
        orm_mode = True

class PrecursorSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class MetaboliteSchema(BaseModel):
    id: int
    precursorId: int
    chemicalId: int
    smiles: str
    formula: str
    inchi: str
    inchikey: str
    alogp: str
    insecticide: float
    herbicide: float
    type: int
    detected: int

    class Config:
        orm_mode = True

class PlateSchema(BaseModel):
    id: int
    name: str
    machineId: int
    experimentId: int

    class Config:
        orm_mode = True

class EnzymeSchema(BaseModel):
    id: int
    metaboliteId: int
    enzyme: str
    biosystem: str
    reactionid: str
    reaction: str

    class Config:
        orm_mode = True

class WellSchema(BaseModel):
    id: int
    name: str
    plateId: int
    precursorId: int
    
    class Config:
        orm_mode = True

class MassSchema(BaseModel):
    id: int
    wellId: int
    metaboliteId: int
    mode: str
    mz: float
    rt: float
    adduct: str
    detected:int
    intensity0hr: float
    intensity24hr: float
    good0hr: float
    good24hr: float
    foldchange: float

    class Config:
        orm_mode = True

class UnknownSchema(BaseModel):
    id: int
    wellId: int
    mz: float
    rt: float
    mode: str
    intensity0hr: float
    intensity24hr: float
    good0hr: float
    good24hr: float
    foldchange: float

    class Config:
        orm_mode = True


