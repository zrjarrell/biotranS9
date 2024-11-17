#generated using sqlacodegen
#command: sqlacodegen sqlite:///biotransdb.db
# coding: utf-8
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Chemical(Base):
    __tablename__ = 'chemical'

    id = Column(Integer, primary_key=True)
    pubchemid = Column(Text, nullable=False, unique=True)
    smiles = Column(Text, nullable=False)
    formula = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    monoisotopic = Column(Float, nullable=False)


class Experiment(Base):
    __tablename__ = 'experiment'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    date = Column(Date, nullable=False)


class Machine(Base):
    __tablename__ = 'machine'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    sensitivity = Column(Float, nullable=False)


class Precursor(Base):
    __tablename__ = 'precursor'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)


class Metabolite(Base):
    __tablename__ = 'metabolite'
    __table_args__ = (
        UniqueConstraint('precursorId', 'chemicalId', 'smiles', 'formula'),
    )

    id = Column(Integer, primary_key=True)
    precursorId = Column(ForeignKey('precursor.id'), nullable=False)
    chemicalId = Column(ForeignKey('chemical.id'), nullable=False)
    smiles = Column(Text, nullable=False)
    formula = Column(Text, nullable=False)
    inchi = Column(Text)
    inchikey = Column(Text)
    alogp = Column(Text)
    insecticide = Column(Float)
    herbicide = Column(Float)
    type = Column(Integer, nullable=False)
    detected = Column(Integer, nullable=False)

    chemical = relationship('Chemical')
    precursor = relationship('Precursor')


class Plate(Base):
    __tablename__ = 'plate'
    __table_args__ = (
        UniqueConstraint('name', 'machineId', 'experimentId'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    machineId = Column(ForeignKey('machine.id'), nullable=False)
    experimentId = Column(ForeignKey('experiment.id'), nullable=False)

    experiment = relationship('Experiment')
    machine = relationship('Machine')


class Enzyme(Base):
    __tablename__ = 'enzyme'
    __table_args__ = (
        UniqueConstraint('metaboliteId', 'enzyme', 'biosystem', 'reactionid'),
    )

    id = Column(Integer, primary_key=True)
    metaboliteId = Column(ForeignKey('metabolite.id'), nullable=False)
    enzyme = Column(Text, nullable=False)
    biosystem = Column(Text, nullable=False)
    reactionid = Column(Text, nullable=False)
    reaction = Column(Text)

    metabolite = relationship('Metabolite')


class Well(Base):
    __tablename__ = 'well'
    __table_args__ = (
        UniqueConstraint('name', 'plateId', 'precursorId'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    plateId = Column(ForeignKey('plate.id'), nullable=False)
    precursorId = Column(ForeignKey('precursor.id'), nullable=False)

    plate = relationship('Plate')
    precursor = relationship('Precursor')


class Mass(Base):
    __tablename__ = 'mass'
    __table_args__ = (
        UniqueConstraint('wellId', 'metaboliteId', 'mz', 'rt', 'mode'),
    )

    id = Column(Integer, primary_key=True)
    wellId = Column(ForeignKey('well.id'), nullable=False)
    metaboliteId = Column(ForeignKey('metabolite.id'), nullable=False)
    mode = Column(Text, nullable=False)
    mz = Column(Float, nullable=False)
    rt = Column(Float, nullable=False)
    adduct = Column(Text, nullable=False)
    detected = Column(Integer, nullable=False)
    intensity0hr = Column(Float)
    intensity24hr = Column(Float)
    good0hr = Column(Float)
    good24hr = Column(Float)
    foldchange = Column(Float)

    metabolite = relationship('Metabolite')
    well = relationship('Well')


class Unknown(Base):
    __tablename__ = 'unknown'
    __table_args__ = (
        UniqueConstraint('wellId', 'mz', 'rt', 'mode'),
    )

    id = Column(Integer, primary_key=True)
    wellId = Column(ForeignKey('well.id'), nullable=False)
    mz = Column(Float, nullable=False)
    rt = Column(Float, nullable=False)
    mode = Column(Text, nullable=False)
    intensity0hr = Column(Float)
    intensity24hr = Column(Float)
    good0hr = Column(Float)
    good24hr = Column(Float)
    foldchange = Column(Float)

    well = relationship('Well')