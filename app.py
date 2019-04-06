import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

engine = create_engine("sqlite:///resources/database.sqlite")

@app.route("/")
def index():
    # Return the homepage.
    return render_template("index.html")

@app.route("/period/<selected_date_1>/<selected_date_2>")
def selected_period_info(selected_date_1, selected_date_2):
    # Return the MDA and MTR prices for a given date.
    days_table = engine.execute(
                                   "SELECT DISTINCT\
                                      DATE(fecha) AS dias\
                                      FROM prices_table\
                                    WHERE dias BETWEEN DATE('" + selected_date_1 + "') AND DATE('" + selected_date_2 + "')"
    )

    period_days = []
    for day in days_table:
        period_days.append(day[0])
    
    table_1 = engine.execute( 
                                "SELECT\
                                   sistema,\
                                   DATE(fecha) AS fecha,\
                                   zona_carga,\
                                   AVG(CAST(precio_mda AS DECIMAL)) AS precio_mda_prom,\
                                   AVG(CAST(precio_energia_mda AS DECIMAL)) AS precio_energia_mda_prom,\
                                   AVG(CAST(precio_perdida_mda AS DECIMAL)) AS precio_perdida_mda_prom,\
                                   AVG(CAST(precio_congestion_mda AS DECIMAL)) AS precio_congestion_mda_prom,\
                                   AVG(CAST(precio_mtr AS DECIMAL)) AS precio_mtr_prom,\
                                   AVG(CAST(precio_energia_mtr AS DECIMAL)) AS precio_energia_mtr_prom,\
                                   AVG(CAST(precio_perdida_mtr AS DECIMAL)) AS precio_perdida_mtr_prom,\
                                   AVG(CAST(precio_congestion_mtr AS DECIMAL)) AS precio_congestion_mtr_prom\
                                 FROM prices_table\
                                 WHERE fecha BETWEEN DATE('" + selected_date_1 + "') AND DATE('" + selected_date_2 + "') AND sistema = 'BCA'\
                                 GROUP BY fecha, zona_carga, sistema\
                                 ORDER BY sistema, fecha"
                                )
    zonas = []
    for row in table_1:
        if row[2] not in zonas:
            zonas.append(row[2])

    precios = ['precio_mda_promedio', 'precio_energia_mda_promedio', 'precio_perdida_mda_promedio', 'precio_congestion_mda_promedio',
               'precio_mtr_promedio', 'precio_energia_mtr_promedio', 'precio_perdida_mtr_promedio', 'precio_congestion_mtr_promedio']

    period_data = {
        'period_days':period_days,
        'zones in system':zonas,
        'dates':{
            day:{
                zone:{
                    precio:[] for precio in precios
                } for zone in zonas
            } for day in period_days
            }
    }
    
    table_1 = engine.execute( 
                                "SELECT\
                                   sistema,\
                                   DATE(fecha) AS fecha,\
                                   zona_carga,\
                                   AVG(CAST(precio_mda AS DECIMAL)) AS precio_mda_prom,\
                                   AVG(CAST(precio_energia_mda AS DECIMAL)) AS precio_energia_mda_prom,\
                                   AVG(CAST(precio_perdida_mda AS DECIMAL)) AS precio_perdida_mda_prom,\
                                   AVG(CAST(precio_congestion_mda AS DECIMAL)) AS precio_congestion_mda_prom,\
                                   AVG(CAST(precio_mtr AS DECIMAL)) AS precio_mtr_prom,\
                                   AVG(CAST(precio_energia_mtr AS DECIMAL)) AS precio_energia_mtr_prom,\
                                   AVG(CAST(precio_perdida_mtr AS DECIMAL)) AS precio_perdida_mtr_prom,\
                                   AVG(CAST(precio_congestion_mtr AS DECIMAL)) AS precio_congestion_mtr_prom\
                                 FROM prices_table\
                                 WHERE fecha BETWEEN DATE('" + selected_date_1 + "') AND DATE('" + selected_date_2 + "') AND sistema = 'BCA'\
                                 GROUP BY fecha, zona_carga, sistema\
                                 ORDER BY sistema, fecha"
                                )
    for row in table_1:
        period_data['dates'][row[1]][row[2]]['precio_mda_promedio'].append(row[3])
        period_data['dates'][row[1]][row[2]]['precio_energia_mda_promedio'].append(row[4])
        period_data['dates'][row[1]][row[2]]['precio_perdida_mda_promedio'].append(row[5])
        period_data['dates'][row[1]][row[2]]['precio_congestion_mda_promedio'].append(row[6])
        period_data['dates'][row[1]][row[2]]['precio_mtr_promedio'].append(row[7])
        period_data['dates'][row[1]][row[2]]['precio_energia_mtr_promedio'].append(row[8])
        period_data['dates'][row[1]][row[2]]['precio_perdida_mtr_promedio'].append(row[9])
        period_data['dates'][row[1]][row[2]]['precio_congestion_mtr_promedio'].append(row[10])
        
    return jsonify(period_data)

@app.route("/period/<selected_date_1>/<selected_date_2>/day/<date>")
def selected_day_info(selected_date_1, selected_date_2, date):

    precios = ['precio_mda_promedio', 'precio_energia_mda_promedio', 'precio_perdida_mda_promedio', 'precio_congestion_mda_promedio',
               'precio_mtr_promedio', 'precio_energia_mtr_promedio', 'precio_perdida_mtr_promedio', 'precio_congestion_mtr_promedio']

    day_data = {
                date: {
                    precio:[] for precio in precios
                }
            }

    table_2 = engine.execute( "SELECT\
                                   DATE(fecha) AS fecha,\
                                   AVG(CAST(precio_mda AS DECIMAL)) AS precio_mda_prom,\
                                   AVG(CAST(precio_energia_mda AS DECIMAL)) AS precio_energia_mda_prom,\
                                   AVG(CAST(precio_perdida_mda AS DECIMAL)) AS precio_perdida_mda_prom,\
                                   AVG(CAST(precio_congestion_mda AS DECIMAL)) AS precio_congestion_mda_prom,\
                                   AVG(CAST(precio_mtr AS DECIMAL)) AS precio_mtr_prom,\
                                   AVG(CAST(precio_energia_mtr AS DECIMAL)) AS precio_energia_mtr_prom,\
                                   AVG(CAST(precio_perdida_mtr AS DECIMAL)) AS precio_perdida_mtr_prom,\
                                   AVG(CAST(precio_congestion_mtr AS DECIMAL)) AS precio_congestion_mtr_prom\
                                 FROM prices_table\
                                 WHERE fecha = DATE('" + date + "')  AND sistema = 'BCA'"
    )

    for row in table_2:
        day_data[date]['precio_mda_promedio'].append(row[1])
        day_data[date]['precio_energia_mda_promedio'].append(row[2])
        day_data[date]['precio_perdida_mda_promedio'].append(row[3])
        day_data[date]['precio_congestion_mda_promedio'].append(row[4])
        day_data[date]['precio_mtr_promedio'].append(row[5])
        day_data[date]['precio_energia_mtr_promedio'].append(row[6])
        day_data[date]['precio_perdida_mtr_promedio'].append(row[7])
        day_data[date]['precio_congestion_mtr_promedio'].append(row[8])

    return jsonify(day_data)

@app.route("/period/<selected_date_1>/<selected_date_2>/day/<date>/zone/<zone>")
def selected_period_days(selected_date_1, selected_date_2, date, zone):

    precios = ['precio_mda_promedio', 'precio_mtr_promedio','precio_mda_max', 'precio_mtr_max']

    week_table = engine.execute(
                                "SELECT DISTINCT\
                                   fecha\
                                FROM prices_table\
                                WHERE DATE(fecha) BETWEEN DATE ('" + date + "', '-6 days') AND DATE('" + date + "')"
    )

    week_days = []
    for day in week_table:
        week_days.append(day[0])

    zone_data = {
        day:{
            precio:[] for precio in precios 
        } for day in week_days
             }

    zone_data['zona'] = zone

    table_3 = engine.execute(
                                "SELECT\
                                   zona_carga,\
                                   fecha,\
                                   AVG(CAST(precio_mda AS DECIMAL)) AS precio_mda_prom,\
                                   AVG(CAST(precio_mtr AS DECIMAL)) AS precio_mtr_prom,\
                                   MAX(CAST(precio_mda AS DECIMAL)) AS precio_mda_max,\
                                   MAX(CAST(precio_mtr AS DECIMAL)) AS precio_mtr_max\
                                FROM prices_table\
                                WHERE DATE(fecha) BETWEEN DATE ('" + date + "', '-6 days') AND DATE('" + date + "') AND zona_carga = '" + zone + "'\
                                GROUP BY zona_carga, fecha"
    )

    for row in table_3:
        zone_data[row[1]]['precio_mda_promedio'].append(row[2])
        zone_data[row[1]]['precio_mtr_promedio'].append(row[3])
        zone_data[row[1]]['precio_mda_max'].append(row[4])
        zone_data[row[1]]['precio_mtr_max'].append(row[5])

    return jsonify(zone_data)

if __name__ == "__main__":
    app.run()
