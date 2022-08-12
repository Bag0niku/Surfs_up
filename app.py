import datetime as dt
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
    <p>Available routes:  <ul>
    <li>/api/v1.0/about </li>
    <li>/api/v1.0/precipitation </li>
    <li>/api/v1.0/stations </li>
    <li>/api/v1.0/temperature </li></ul></p>
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

@app.route("/api/v1.0/temperature")
def temperature():
    last_year = dt.datetime(2017, 8,23) - dt.timedelta(days=365)
    temps_last_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>= last_year).filter(Measurement.station == 'USC00519281').all()
    temps = {date:temp for date, temp in temps_last_year} 
    return jsonify(temps = temps)

if __name__ == "__main__":
    app.run(debug=True)
