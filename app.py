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


hello_list = ["Hello", "World!"]
hello_dict = {"Hello": "World!"}


@app.route("/")
def welcome():
    return (""" 
    <h1>Welcome to the Climate Analysis of Ouahu, Hawaii API! </h1>
    <p><b>Available routes:</b>  &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;  &nbsp; &nbsp;&nbsp; &nbsp;  &nbsp; &nbsp;&nbsp;  &nbsp; &nbsp; <b>Descriptions:</b>
    <ul>
    <li>/api/v1.0/precipitation  &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp;
                            Rainfall last year.</li>
    <li>/api/v1.0/stations        &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;   
                            The list of active stations.</li>    
    <li>/api/v1.0/temperatures    &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  
                            The temperatures from last year.</li>
    <li> /api/v1.0/temp/start/end   &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 
                            Find the minimum, average and maximum temeratures over a given time period from the most active station.</li>
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

@app.route("/api/v1.0/stations")
def station():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/temperatures")
def temp():
    last_year = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    temps_last_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=last_year).all()
    temps = {date:temp for date, temp in rain_last_year}
    return jsonify(rain)



@app.route("/api/v1.0/temp/<start>/<end>")
def temp_stats(start, end):
    select = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs) ]
    last_year = dt.datetime(2017, 8,23) - dt.timedelta(days=365)
    if end is False:
        results = session.query(*select).filter(Measurement.date>=start).all()
    # if (start and end) != None:
    #     s = f"\n  start and end  ||  START = {type(start)}  || END = {type(end)}"
    # elif start and not end:
    #     s = f"\n  Start only  ||  START = {type(start)}  || END = {type(end)}"
    # elif end and not start:
    #     s = f"\n  End only  ||  START = {type(start)}  || END = {type(end)}"  
    else: 
        # s = f"\n  No Start or End  ||  START = {type(start)}  || END = {type(end)}"
        # temps_last_year = session.query(*select).filter(Measurement.date>= last_year).filter(Measurement.station == 'USC00519281').all()
        results = session.query(*select).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    # temps = [row for row in spam]
    temps = list(np.ravel(results))
    return jsonify(temps=temps)#, info=s)

if __name__ == "__main__":
    app.run(debug=True)
