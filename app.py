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


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///resources/database.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
zones = Base.classes.zones_catalogue
prices = Base.classes.prices_table



@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/period/<selected_date_1>/<selected_date_2>")
def selected_period_info(selected_date):
    """Return the MDA and MTR prices for a given date."""
    sel = [
        prices.sistema,
        prices.zona_carga,
        func.date(prices.fecha).label('fecha'),
        func.avg(prices.precio_mda).label('precio_mda_promedio'),
        func.avg(prices.precio_energia_mda).label('precio_energia_mda_promedio'),
        func.avg(prices.precio_perdida_mda).label('precio_perdida_mda_promedio'),
        func.avg(prices.precio_congestion_mda).label('precio_congestion_mda_promedio'),
        func.avg(prices.precio_mtr).label('precio_mtr_promedio'),
        func.avg(prices.precio_energia_mtr).label('precio_energia_mtr_promedio'),
        func.avg(prices.precio_perdida_mtr).label('precio_perdida_mtr_promedio'),
        func.avg(prices.precio_congestion_mtr).label('precio_congestion_mtr_promedio')
    ]

    results = db.session.query(*sel).\
        filter(prices.fecha == func.date(selected_date)).\
            group_by(func.date(prices.fecha)).all()

    dates_qry = db.session.query(prices.fecha.distinct()).\
        filter(prices.fecha >= selected_date_1).\
        filter(prices.fecha <= selected_date_2).all()

    # Create a dictionary entry for each entry
    period_data = {}
    for result in results:
        period_data["sistema"] = result[0]
        period_data["zona_carga"] = result[1]
        period_data["fecha"] = result[2]
        period_data["precio_mda_promedio"] = result[3]
        period_data["precio_energia_mda_promedio"] = result[4]
        period_data["precio_perdida_mda_promedio"] = result[5]
        period_data["precio_congestion_mda_promedio"] = result[6]
        period_data["precio_mtr_promedio"] = result[7]
        period_data["precio_energia_mtr_promedio"] = result[8]
        period_data["precio_perdida_mtr_promedio"] = result[9]
        period_data["precio_congestion_mtr_promedio"] = result[10]

    print(period_data)
    return jsonify(period_data)

@app.route("/<date>")
def selected_period_days():
    """Return a list of sample names."""

    sel_1 = [
        func.avg(prices.precio_energia_mda).label('precio_energia_mda_promedio'),
        func.avg(prices.precio_perdida_mda).label('precio_perdida_mda_promedio'),
        func.avg(prices.precio_congestion_mda).label('precio_congestion_mda_promedio'),
        func.avg(prices.precio_energia_mtr).label('precio_energia_mtr_promedio'),
        func.avg(prices.precio_perdida_mtr).label('precio_perdida_mtr_promedio'),
        func.avg(prices.precio_congestion_mtr).label('precio_congestion_mtr_promedio')
    ]

    results_1 = db.session.query(*sel_1).\
        filter(prices.fecha == date).\
            group_by(prices.fecha).all()    

    sel_2 = [
        prices.zona_carga,
        prices.fecha,
        func.avg(prices.precio_mda).label('precio_mda_promedio'),
        func.avg(prices.precio_mtr).label('precio_mtr_promedio')        
    ]

    results_1 = db.session.query(*sel_2).\
        filter(prices.fecha == date).\
            group_by(prices.fecha).all()    


    day_data = {}
    for result in results:
        period_data["fecha"] = result[2]
        period_data["precio_mda_promedio"] = result[3]
        period_data["precio_energia_mda_promedio"] = result[4]
        period_data["precio_perdida_mda_promedio"] = result[5]
        period_data["precio_congestion_mda_promedio"] = result[6]
        period_data["precio_mtr_promedio"] = result[7]
        period_data["precio_energia_mtr_promedio"] = result[8]
        period_data["precio_perdida_mtr_promedio"] = result[9]
        period_data["precio_congestion_mtr_promedio"] = result[10]


    # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])

if __name__ == "__main__":
    app.run()
