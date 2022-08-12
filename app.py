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

@app.route("/precipitation")
def prcp():
    return str(hello_list)

@app.route("/stations")
def station():
    return jsonify(hello_list)

@app.route("/temperature")
def temperature():
    return hello_dict

if __name__ == "__main__":
    app.run(debug=True)
