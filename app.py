import datetime as dt
from statistics import mean
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



#start the Flask app
app = Flask(__name__)

## Prepare the database
hawaii = r"sqlite:///hawaii.sqlite"
engine = create_engine(hawaii)
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

@app.route("/")
def welcome():
    return (""" 
    <head>
        <style>
            td {padding:5px 50px 0px 0px}
        </style>
    </head>
    <body>
        <h1>Welcome to the Climate Analysis of Ouahu, Hawaii API! </h1>
        <table>
            <tr>
                <th style='text-align:left'>Available routes:</th>
                <th style='text-align:left'>Descriptions:</th>
            </tr>
        
            <tr>
                <td>/api/v1.0/rain  </td>
                <td> Rainfall last year. </td>
            </tr>
            <tr>
                <td> /api/v1.0/rain/start/end </td>
                <td> Find the minimum, average and maximum precipitaion measurements over a given time period.</td>
            </tr>
            <tr>
                <td>/api/v1.0/stations </td>
                <td>The list of active stations.</td>
            </tr>    
            <tr>
                <td>/api/v1.0/stations/activity  </td>
                <td>The list of active stations and the number of readings within the dataset.</td>
            </tr>    
            <tr>
                <td>/api/v1.0/stations/all_data    </td>
                <td> All the data in the dataset organized by station.</td>
            </tr>    
            <tr>
                <td>/api/v1.0/temperatures    </td>
                <td>The temperatures from last year.</td>
            </tr>
            <tr> 
                <td>/api/v1.0/temp/start/end </td>
                <td>Find the minimum, average and maximum temeratures over a given time period.</td>
            </tr>
        </table>
    </body>""")


@app.route("/about")
def spam():
    return "Hi"

@app.route("/api/v1.0/rain")
def prcp():
    last_year = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    rain_last_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=last_year).all()
    rain = {date:prcp for date, prcp in rain_last_year}
    return jsonify(rain)


@app.route("/api/v1.0/rain/<start>/<end>")
def rain_stats(start, end):
    if end is False:
        results = engine.execute(f"SELECT MIN(prcp), AVG(prcp), MAX(prcp) FROM measurement WHERE date='{start}' ;")
    else: 
        results = engine.execute(f"SELECT MIN(prcp), AVG(prcp), MAX(prcp) FROM measurement WHERE date BETWEEN '{start}' AND '{end}' ;")
    
    rain = [{"Minimum" : r[0], "Average": r[1], "Maximum": r[2]} for r in results]
    return jsonify(prcp=rain)



@app.route("/api/v1.0/stations")
def station():
    results = engine.execute("SELECT * FROM station;")
    
    stations =[{"station":r[1], "name":r[2], "Latitude":r[3], "Longitude":r[4], "Elevation":r[5]} for r in results]
    return jsonify(stations=stations)

@app.route("/api/v1.0/temperatures")
def temp():
    last_year = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    temps_last_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=last_year).all()
    temps = {date:temp for date, temp in temps_last_year}
    return jsonify(temps)



@app.route("/api/v1.0/temp/<start>/<end>")
def temp_stats(start, end):
    
    if end is False:
        results = engine.execute(f"SELECT MIN(tobs), AVG(tobs), MAX(tobs) FROM measurement WHERE date='{start}';")
    else: 
        results = engine.execute(f"SELECT MIN(tobs), AVG(tobs), MAX(tobs) FROM measurement WHERE date BETWEEN '{start}' AND '{end}';")
    temp = [{"Minimum" : x[0], "Average" :x[1], "Maximum": x[2]} for x in results]
    

    return jsonify(temps=temp)

@app.route("/api/v1.0/stations/all_data")
def all_data():
    all = dict()
    results = engine.execute(f"SELECT * FROM station;")
    for id, station, name, lat, lon, elev in results:
        d = {"name": name, "measurements": dict(), "Latitude":lat, "Longitude":lon, "elevation":elev}
        for r in engine.execute(f"SELECT prcp, tobs FROM measurement WHERE station = '{station};'"):
            d["measurements"][r[2]] = {"prcp": r[3] , "tobs":r[4]}
        all[station] = d
    
    return jsonify(all)


@app.route("/api/v1.0/stations/activity")
def active_stations():
    results =  session.execute("SELECT station, COUNT(id) AS activity FROM measurement GROUP BY station ORDER BY activity DESC;")
    active_count = [{"station":row[0], "activity":row[1]} for row in results]
    return jsonify(activity=active_count)








if __name__ == "__main__":
    app.run(debug=True)
