# Create zones catalogue
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

# Create master tables
import numpy as np
import requests
import json
import os

P_NodesDF = P_NodesDF.loc[P_NodesDF["zona_carga"] != "No Aplica", :]        # Drop rows with unassigned ZONA DE CARGA

# Count unique ZONA DE CARGA for each SISTEMA
Zonas_CargaDF = P_NodesDF.loc[:, ["sistema", "zona_carga"]]
Zonas_CargaDF = Zonas_CargaDF.drop_duplicates()
Zonas_CargaDF_Count = Zonas_CargaDF.groupby("sistema").count()

# Count Unique NODO P for each SISTEMA
NodosDF = P_NodesDF.loc[:, ["sistema", "nombre_nodo_p"]]
NodosDF = NodosDF.drop_duplicates()
NodosDF_Count = NodosDF.groupby("sistema").count()

# Retrieve names for ZONA and save to lists
BCA_ZonasLS = P_NodesDF.loc[P_NodesDF["sistema"] == "BCA", "zona_carga"]
BCA_ZonasLS = BCA_ZonasLS.drop_duplicates()
BCA_ZonasLS = BCA_ZonasLS.tolist()

BCS_ZonasLS = P_NodesDF.loc[P_NodesDF["sistema"] == "BCS", "zona_carga"]
BCS_ZonasLS = BCS_ZonasLS.drop_duplicates()
BCS_ZonasLS = BCS_ZonasLS.tolist()

SIN_ZonasLS = P_NodesDF.loc[P_NodesDF["sistema"] == "SIN", "zona_carga"]
SIN_ZonasLS = SIN_ZonasLS.drop_duplicates()
SIN_ZonasLS = SIN_ZonasLS.tolist()

# Create lists to build API Requests
year = "2018"
Calendar_LS = []

for month in range(1,13):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        for day in range(1,32):
            if day < 10 and month < 10:
                date = f"{year}/0{str(month)}/0{str(day)}"
                Calendar_LS.append(date)
            elif day < 10 and month >= 10:
                date = f"{year}/{str(month)}/0{str(day)}"
                Calendar_LS.append(date)
            elif day >= 10 and month < 10:
                date = f"{year}/0{str(month)}/{str(day)}"
                Calendar_LS.append(date)
            elif day >= 10 and month >= 10:
                date = f"{year}/{str(month)}/{str(day)}"
                Calendar_LS.append(date)
    elif month in [4, 6, 9, 11]:
        for day in range(1,31):
            if day < 10 and month < 10:
                date = f"{year}/0{str(month)}/0{str(day)}"
                Calendar_LS.append(date)
            elif day < 10 and month >= 10:
                date = f"{year}/{str(month)}/0{str(day)}"
                Calendar_LS.append(date)
            elif day >= 10 and month < 10:
                date = f"{year}/0{str(month)}/{str(day)}"
                Calendar_LS.append(date)
            elif day >= 10 and month >= 10:
                date = f"{year}/{str(month)}/{str(day)}"
                Calendar_LS.append(date)       
    else:
        for day in range(1,29):
            if day < 10 and month < 10:
                date = f"{year}/0{str(month)}/0{str(day)}"
                Calendar_LS.append(date)
            elif day < 10 and month >= 10:
                date = f"{year}/{str(month)}/0{str(day)}"
                Calendar_LS.append(date)
            elif day >= 10 and month < 10:
                date = f"{year}/0{str(month)}/{str(day)}"
                Calendar_LS.append(date)
            elif day >= 10 and month >= 10:
                date = f"{year}/{str(month)}/{str(day)}"
                Calendar_LS.append(date)

# Create dictionary for SISTEMA-ZONAS
Sistemas_dict = {"BCA":BCA_ZonasLS, "BCS":BCS_ZonasLS, "SIN":SIN_ZonasLS}
LS_SIN_ZonasLS = []
Zonas_aux = []
flag_sist = 0
while flag_sist < len(Sistemas_dict["SIN"]):
    if flag_sist in [9, 19, 29, 39, 49, 59, 69, 79, 89, 99]:
        zn = Sistemas_dict["SIN"][flag_sist]
        Zonas_aux.append(zn)
        LS_SIN_ZonasLS.append(Zonas_aux)
        Zonas_aux = []
        flag_sist += 1
    else:
        zn = Sistemas_dict["SIN"][flag_sist]
        Zonas_aux.append(zn)
        flag_sist += 1
    if flag_sist == 100:
        Zonas_aux = []   
        zn = Sistemas_dict["SIN"][flag_sist]
        Zonas_aux.append(zn)
        LS_SIN_ZonasLS.append(Zonas_aux)
        break
Sistemas_dict["SIN"] = LS_SIN_ZonasLS

#Create Lists for API Requests - MDA               
Sistemas_MDA = []
Zonas_MDA = []
Fechas_MDA = []
Horas_MDA = []
pz_MDA = []
pz_ene_MDA = []
pz_per_MDA = []
pz_cng_MDA = []

# Make API requests - MDA
# Sistemas BC y BCS 

# print("----------------------------------------------------------------------------")
# print(                     "Retrieving data for MDA-BC, MDA-BS")
# print("----------------------------------------------------------------------------")

TEST = 0

for SISTEMA in Sistemas_dict:
    
    if SISTEMA != "SIN":      
        
        ZONAS= Sistemas_dict[SISTEMA]
        ZTEXT = ','.join(ZONAS)
           
        n = 0
        
        while n < 365:
            if n == 364:
                DUNO = Calendar_LS[n]
                DDOS = Calendar_LS[n]
                THoras = 24
            else:
                
                DUNO = Calendar_LS[n]
                DDOS = Calendar_LS[n+6]
                THoras = 168
            
            url_new = f"https://ws01.cenace.gob.mx:8082/SWPEND/SIM/{SISTEMA}/MDA/{ZTEXT}/{DUNO}/{DDOS}/JSON"
            url_new= url_new.replace(" ","-")
            response = requests.get(url_new)
            response_JSON = response.json()
            
            if response_JSON["status"] == "OK":
                
                for Z in range(len(ZONAS)):
                    
                    for HORA in range(THoras):
                        
                        Sistemas_MDA.append(response_JSON["sistema"])
                        Zonas_MDA.append(response_JSON["Resultados"][Z]["zona_carga"])
                        try:
                            Fechas_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["fecha"])
                        except: 
                            Fechas_MDA.append("NULL")
                        try: 
                            Horas_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["hora"])
                        except: 
                            Horas_MDA.append("NULL")
                        try:
                            pz_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz"])
                        except:
                            pz_MDA.append("NULL")
                        try:
                            pz_ene_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_ene"])
                        except:
                            pz_ene_MDA.append("NULL")
                        try:
                            pz_per_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_per"])
                        except:
                            pz_per_MDA.append("NULL")
                        try:
                            pz_cng_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_cng"])
                        except:
                            pz_cng_MDA.append("NULL")
            n= n + 7
            TEST= TEST+1
            # print(f"Processing: MDA | {SISTEMA} |{ZONAS} | TEST:{TEST}  ")

# print("----------------------------------------------------------------------------")
# print(                  "Finished Retrieving data for MDA-BC, MDA-BS")
# print("----------------------------------------------------------------------------")

#Dataframe for MDA prices
MT_DF_MDA = pd.DataFrame({
    "sistema":Sistemas_MDA,
    "zona_carga":Zonas_MDA,
    "fecha":Fechas_MDA,
    "hora":Horas_MDA,
    "precio_mda":pz_MDA,
    "precio_energia_mda":pz_ene_MDA,
    "precio_perdida_mda":pz_per_MDA,
    "precio_congestion_mda":pz_cng_MDA,
})
MT_DF_MDA = MT_DF_MDA.sort_values(["sistema","zona_carga","fecha"], ascending=[True, True,True])
# MT_DF_MDA.head()

#Create Lists for API Requests - MTR               
Sistemas_MTR = []
Zonas_MTR = []
Fechas_MTR = []
Horas_MTR = []
pz_MTR = []
pz_ene_MTR = []
pz_per_MTR = []
pz_cng_MTR = []

# Make API requests - MTR
#Sistemas BC y BCS 

# print("----------------------------------------------------------------------------")
# print(                  "Retrieving data for MTR-BC, MTR-BS")
# print("----------------------------------------------------------------------------")

TEST = 0

for SISTEMA in Sistemas_dict:
    
    if SISTEMA != "SIN":      
        
        ZONAS= Sistemas_dict[SISTEMA]
        ZTEXT = ','.join(ZONAS)
           
        n = 0
        
        while n < 365:
            if n == 364:
                DUNO = Calendar_LS[n]
                DDOS = Calendar_LS[n]
                THoras = 24
            else:
                
                DUNO = Calendar_LS[n]
                DDOS = Calendar_LS[n+6]
                THoras = 168
            
            url_new = f"https://ws01.cenace.gob.mx:8082/SWPEND/SIM/{SISTEMA}/MTR/{ZTEXT}/{DUNO}/{DDOS}/JSON"
            url_new= url_new.replace(" ","-")
            response = requests.get(url_new)
            response_JSON = response.json()
            
            if response_JSON["status"] == "OK":
                
                for Z in range(len(ZONAS)):
                    
                    for HORA in range(THoras):
                        
                        Sistemas_MTR.append(response_JSON["sistema"])
                        Zonas_MTR.append(response_JSON["Resultados"][Z]["zona_carga"])
                        try:
                            Fechas_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["fecha"])
                        except: 
                            Fechas_MTR.append("NULL")
                        try: 
                            Horas_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["hora"])
                        except: 
                            Horas_MTR.append("NULL")
                        try:
                            pz_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz"])
                        except:
                            pz_MTR.append("NULL")
                        try:
                            pz_ene_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_ene"])
                        except:
                            pz_ene_MTR.append("NULL")
                        try:
                            pz_per_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_per"])
                        except:
                            pz_per_MTR.append("NULL")
                        try:
                            pz_cng_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_cng"])
                        except:
                            pz_cng_MTR.append("NULL")
            n= n + 7
            TEST= TEST+1
            # print(f"Processing: MTR | {SISTEMA} |{ZONAS} | TEST:{TEST} ")

# print("----------------------------------------------------------------------------")
# print(               "Finished Retrieving data for MTR-BC, MTR-BCS")
# print("----------------------------------------------------------------------------")

#Dataframe for MTR prices
MT_DF_MTR = pd.DataFrame({
    "sistema":Sistemas_MTR,
    "zona_carga":Zonas_MTR,
    "fecha":Fechas_MTR,
    "hora":Horas_MTR,
    "precio_mtr":pz_MTR,
    "precio_energia_mtr":pz_ene_MTR,
    "precio_perdida_mtr":pz_per_MTR,
    "precio_congestion_mtr":pz_cng_MTR,
})
MT_DF_MTR = MT_DF_MTR.sort_values(["sistema","zona_carga","fecha"], ascending=[True, True,True])
# MT_DF_MTR.head()

# Create merged prices table
prices_df = MT_DF_MDA.merge(MT_DF_MTR, on=['sistema','zona_carga','fecha','hora'], how='inner')
# prices_df.head()

# Create database and tables
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

class Prices_Table(Base):
    __tablename__ = 'prices_table'
    id = Column(Integer, primary_key=True)
    sistema = Column(String(50))
    zona_carga = Column(String(50))
    fecha = Column(String(50)) # Revisar!!!!! 
    hora = Column(Integer)  # Revisar!!!!!
    precio_mda = Column(Float)
    precio_energia_mda = Column(Float)
    precio_perdida_mda = Column(Float)
    precio_congestion_mda = Column(Float)
    precio_mtr = Column(Float)
    precio_energia_mtr = Column(Float)
    precio_perdida_mtr = Column(Float)
    precio_congestion_mtr = Column(Float)

# Create Database Connection
engine = create_engine('sqlite:///../../resources/database.sqlite')
conn = engine.connect()
Base.metadata.create_all(engine)

from sqlalchemy.orm import Session
session = Session(bind=engine)

P_NodesDF.to_sql('zones_catalogue', engine, if_exists='replace', index_label='id')

prices_df.to_sql('prices_table', engine, if_exists='replace', index_label='id')