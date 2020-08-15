# import SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import numpy and datetime
import numpy as np
import datetime as dt

# import flask
from flask import Flask, jsonify

engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect existing database
Base = automap_base()

# reflect existing tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# create Flask app
app = Flask(__name__)

# home
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/ api/v1.0/<start><br/>"
        f"/ api/v1.0/<start>/<end><br/>"
    )

# precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(
        (Measurement.date).desc()).all()
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    date_prcp = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= one_year_ago).all()

    session.close()

    # Convert list of tuples into normal list
    all_date_prcp = list(np.ravel(date_prcp))

    return jsonify(all_date_prcp)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).limit(1).all()

    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    last_year_tobs = session.query(Measurement.tobs).\
        filter(Measurement.station=active_station).filter(Measurement.date >= one_year_ago).all()

    session.close()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(last_year_tobs))

    return jsonify(tobs)


# debug
if __name__ == '__main__':
    app.run(debug=True)
