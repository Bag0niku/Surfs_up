from email import message
from flask import Flask
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

## Prepare the database
hawaii = r"sqlite///:hawaii.sqlite"
engine = create_engine(hawaii)
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

## Start the flask app
app = Flask(__name__)

# The main page
app.route("/")
def welcome():
    message = """ Welcome to the Climate Analysis of Ouahu, Hawaii API!
                 Available routes:
                 /about
                 /precipitation
                 /stations
                 /temperature

        
        """

# The about page
app.route("/about")


if __name__ == __main__:
    app.run(debug=True)

