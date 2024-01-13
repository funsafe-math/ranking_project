from sqlalchemy import create_engine, ForeignKey, Column, String, CHAR, Integer, Boolean, Float, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Rankings(Base):
    __tablename__ = 'Rankings'
    ranking_id = Column(Integer, unique=True, primary_key=True)
    description = Column(String)
    expiring = Column(Integer)

class Criteria(Base):
    __tablename__ = 'Criteria'
    criteria_id = Column(Integer, unique = True, primary_key = True)
    ranking_id = Column(Integer, ForeignKey("Rankings.ranking_id"))
    name = Column(String)
    description = Column(String)

class Variables(Base):
    __tablename__ = 'Variables'
    variable_id = Column(Integer,primary_key=True)
    ranking_method = Column(String)
    aggregation_method = Column(String)
    completness_required = Column(Boolean)
    ranking_id = Column(Integer, ForeignKey("Rankings.ranking_id"))

class Scale(Base):
    __tablename__ = 'Scale'
    scale_id = Column(Integer, primary_key = True)
    description = Column(String)
    value = Column(Float)
    ranking_id = Column(Integer, ForeignKey("Rankings.ranking_id"))

class Weights(Base):
    __tablename__ = 'Weights'
    weights_id = Column(Integer, primary_key=True)
    ranking_id = Column(Integer, ForeignKey("Rankings.ranking_id"))
    expert_id = Column(Integer, ForeignKey("Experts.expert_id"))
    criteria_id = Column(Integer, ForeignKey("Criteria.criteria_id"))
    scale_id = Column(Integer, ForeignKey("Scale.scale_id"))
    weights = Column(JSON)

class Data(Base):
    __tablename__ = 'Data'
    data_id = Column(Integer, primary_key=True)
    ranking_id = Column(Integer, ForeignKey("Rankings.ranking_id"))
    expert_id = Column(Integer, ForeignKey("Experts.expert_id"))
    criteria_id = Column(Integer, ForeignKey("Criteria.criteria_id"))
    alternative1_id = Column(Integer)
    alternative2_id = Column(Integer)
    result = Column(Boolean)

class Alternatives(Base):
    __tablename__ = 'Alternatives'
    alternative_id = Column(Integer, primary_key = True)
    ranking_id = Column(Integer, ForeignKey("Rankings.ranking_id"))
    name = Column(String)
    description = Column(String)

class Experts(Base):
    __tablename__ = 'Experts'
    expert_id = Column(Integer,primary_key = True)
    ranking_id = Column(Integer, ForeignKey("Rankings.ranking_id"))
    name = Column(String)
    email = Column(String)

class Results(Base):
    __tablename__ = 'Results'
    results_id = Column(Integer,primary_key=True)
    ranking_id = Column(Integer, ForeignKey("Rankings.ranking_id"))
    alternative_id = Column(Integer, ForeignKey("Alternatives.alternative_id"))
    place = Column(Integer)

engine = create_engine("sqlite:///mydb.db", echo = True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind = engine)
session = Session()




