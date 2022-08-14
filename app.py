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
    <h1>Welcome to the Climate Analysis of Ouahu, Hawaii API! </h1>
    <p><b>Available routes:</b>  &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;  &nbsp; &nbsp;&nbsp; &nbsp;  &nbsp; &nbsp;&nbsp;  &nbsp; &nbsp; <b>Descriptions:</b>
    <ul>
    <li>/api/v1.0/precipitation  &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp;
                            Rainfall last year.
                            </li>
    <li>/api/v1.0/stations        &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;   
                            The list of active stations.
                            </li>    
    <li>/api/v1.0/temperatures    &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  
                            The temperatures from last year.
                            </li>
    <li> /api/v1.0/temp/start/end   &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 
                            Find the minimum, average and maximum temeratures over a given time period from the most active station.
                            </li>
    </ul></p>
    """)


@app.route("/about")
def spam():
    return "Hi"

@app.route("/api/v1.0/precipitation")
def prcp():
    last_year = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    rain_last_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=last_year).all()
    rain = {date:prcp for date, prcp in rain_last_year}
    return jsonify(rain)


@app.route("/api/v1.0/rain/<start>/<end>")
def rain_stats(start, end):
    select = [func.min(Measurement.prcp), func.avg(Measurement.prcp), func.max(Measurement.prcp)]
    last_year = dt.datetime(2017, 8,23) - dt.timedelta(days=365)
    if (start is False) and (end is False):
        return "Dates are needed to see the temperature statistics." 
    elif end is False:
        results = session.query(*select).filter(Measurement.date>=start).all()
    else: 
        results = session.query(*select).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    
    rain = [{"Minimum" : r[0], "Average": r[1], "Maximum": r[2]} for r in results]



@app.route("/api/v1.0/stations")
def station():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/temperatures")
def temp():
    last_year = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    temps_last_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=last_year).all()
    temps = {date:temp for date, temp in temps_last_year}
    return jsonify(temps)



@app.route("/api/v1.0/temp/<start>/<end>")
def temp_stats(start, end):
    select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    last_year = dt.datetime(2017, 8,23) - dt.timedelta(days=365)
    if (start is False) and (end is False):
        return "Dates are needed to see the temperature statistics." 
    elif end is False:
        results = session.query(*select).filter(Measurement.date>=start).all()
    else: 
        results = session.query(*select).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    temps = list(np.ravel(results))
    temp = {"Minimum" : temps[0], "Average"] :temps[1], "Maximum": temps[2]}
    

    return jsonify(temps=temp)#, info=s)


@app.route("/api/v1.0/stations/all_data")
def all_data():
    all = dict()
    results = engine.execute(f"SELECT * FROM station;")
    for id, station, name, lat, lon, elev in results:
        d = dict{"name": name, "measurements": dict(), "Latitude":lat, "Longitude":lon, "elevation":elev}
        place = engine.execute(f"SELECT * FROM measurement WHERE station = '{station};'")
        for r in results:
            d["measurements"][r[2]] = {"prcp": r[3] , "tobs":r[4]}
        all[station] = d
    
    return jsonify(all)


@app.route("/api/v1.0/stations/activity")
def active_stations():
    activity = [{"station":row[0], "activity":row[1]} for row in session.execute("SELECT COUNT(id) AS activity FROM measurement GROUP BY station ORDER BY activity DESC;")]
    return jsonify(activity=activity)








if __name__ == "__main__":
    app.run(debug=True)
