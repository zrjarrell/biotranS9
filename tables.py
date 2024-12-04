from sqlalchemy import MetaData, Table, Column, Date, Float, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.sql import select
from sqlalchemy.orm import relationship

metadata = MetaData()

chemical = Table(
    "chemical",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pubchemid", Text, nullable=False, unique=True),
    Column("smiles", Text, nullable=False),
    Column("formula", Text, nullable=False),
    Column("name", Text, nullable=False),
    Column("monoisotopic", Float, nullable=False),
)

experiment = Table(
    "experiment",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False, unique=True),
    Column("data", Date, nullable=False),
)

machine = Table(
    "machine",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False, unique=True),
    Column("sensitivity", Float, nullable=False),
)

precursor = Table(
    "precursor",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False, unique=True),
)

metabolite = Table(
    "metabolite",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("precursorId", ForeignKey('precursor.id'), nullable=False),
    Column("chemicalId", ForeignKey('chemical.id'), nullable=False),
    Column("smiles", Text, nullable=False),
    Column("formula", Text, nullable=False),
    Column("inchi", Text),
    Column("inchikey", Text),
    Column("alogp", Text),
    Column("insecticide", Float),
    Column("herbicide", Float),
    Column("type", Integer, nullable=False),
    Column("detected", Integer, nullable=False),

    UniqueConstraint("precursorId", "chemicalId", "smiles", "formula"),
)

plate = Table(
    "plate",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("machineId", ForeignKey('machine.id'), nullable=False),
    Column("experimentId", ForeignKey('experiment.id'), nullable=False),

    UniqueConstraint("name", "machineId", "experimentId"),
)

enzyme = Table(
    "enzyme",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("metaboliteId", ForeignKey('metabolite.id'), nullable=False),
    Column("enzyme", Text, nullable=False),
    Column("biosystem", Text, nullable=False),
    Column("reactionid", Text, nullable=False),
    Column("reaction", Text),

    UniqueConstraint("metaboliteId", "enzyme", "biosystem", "reactionid"),
)

well = Table(
    "well",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("plateId", ForeignKey('plate.id'), nullable=False),
    Column("precursorId", ForeignKey('precursor.id'), nullable=False),

    UniqueConstraint("name", "plateId", "precursorId"),
)

mass = Table(
    "mass",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("wellId", ForeignKey('well.id'), nullable=False),
    Column("metaboliteId", ForeignKey('metabolite.id'), nullable=False),
    Column("mode", Text, nullable=False),
    Column("mz", Float, nullable=False),
    Column("rt", Float, nullable=False),
    Column("adduct", Text, nullable=False),
    Column("detected", Integer, nullable=False),
    Column("intensity0hr", Float),
    Column("intensity24hr", Float),
    Column("good0hr", Float),
    Column("good24hr", Float),
    Column("foldchange", Float),

    UniqueConstraint("wellId", "metaboliteId", "mz", "rt", "mode"),
)

unknown = Table(
    "unknown",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("wellId", ForeignKey('well.id'), nullable=False),
    Column("mz", Float, nullable=False),
    Column("rt", Float, nullable=False),
    Column("mode", Text, nullable=False),
    Column("intensity0hr", Float),
    Column("intensity24hr", Float),
    Column("good0hr", Float),
    Column("good24hr", Float),
    Column("foldchange", Float),

    UniqueConstraint("wellId", "mz", "rt", "mode"),
)