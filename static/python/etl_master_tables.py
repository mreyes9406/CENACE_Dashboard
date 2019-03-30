
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float
import pymysql
pymysql.install_as_MySQLdb()

Base = declarative_base()

class Zones_Catalogue(Base):
    __tablename__ = 'zones_catalogue'
    id = Column(Integer, primary_key=True)
    sistema = Column(String(50))
    centro_control_regional = Column(String(50))
    zona_carga = Column(String(50))
    clave_nodo_p = Column(String(50))
    nombre_nodo_p = Column(String(50))
    nivel_tension_kV = Column(Float)
    carga_directamente_modelada = Column(String(50))
    carga_indirectamente_modelada = Column(String(50))
    gen_directamente_modelada = Column(String(50))
    gen_indirectamente_modelada = Column(String(50))
    zona_operacion = Column(String(50))
    gerencia_reg_trans = Column(String(50))
    zona_distribucion = Column(String(50))
    gerencia_div_dist = Column(String(50))
    cve_entidad_fed = Column(Integer)
    entidad_fed = Column(String(50))
    cve_municipio = Column(Integer)
    municipio = Column(String(50))
    reg_trans = Column(String(50))

# Create Database Connection
engine = create_engine('sqlite:///../../resources/database.sqlite')
conn = engine.connect()
Base.metadata.create_all(engine)

from sqlalchemy.orm import Session
session = Session(bind=engine)

# Create zones catalogue and upload to database
import pandas as pd

P_NodesXLSX = "../../resources/Catalogo_NodosP_Sistema_Electrico_Nacional_v2018_12_19.xlsx"
P_NodesDF = pd.read_excel(P_NodesXLSX, header=1)
P_NodesDF = P_NodesDF.rename(columns={
                                      "SISTEMA":"sistema",
                                      "CENTRO DE CONTROL REGIONAL":"centro_control_regional",
                                      "ZONA DE CARGA":"zona_carga",
                                      "CLAVE":"clave_nodo_p",
                                      "NOMBRE":"nombre_nodo_p",
                                      "NIVEL DE TENSIÓN (kV)":"nivel_tension_kV",
                                      "DIRECTAMENTE MODELADA":"carga_directamente_modelada",
                                      "INDIRECTAMENTE MODELADA":"carga_indirectamente_modelada",
                                      "DIRECTAMENTE MODELADA.1":"gen_directamente_modelada",
                                      "INDIRECTAMENTE MODELADA.1":"gen_indirectamente_modelada",
                                      "ZONA DE OPERACIÓN DE TRANSMISIÓN":"zona_operacion",
                                      "GERENCIA REGIONAL DE TRANSMISIÓN":"gerencia_reg_trans",
                                      "ZONA DE DISTRIBUCIÓN":"zona_distribucion",
                                      "GERENCIA DIVISIONAL DE DISTRIBUCIÓN":"gerencia_div_dist",
                                      "CLAVE DE ENTIDAD FERERATIVA (INEGI)":"cve_entidad_fed",
                                      "ENTIDAD FERERATIVA (INEGI)":"entidad_fed",
                                      "CLAVE DE MUNICIPIO (INEGI)":"cve_municipio",
                                      "MUNICIPIO (INEGI)":"municipio",
                                      "REGION DE TRANSMISION":"reg_trans",
                                     })
P_NodesDF.to_sql('zones_catalogue', engine, if_exists='replace', index_label='id')


