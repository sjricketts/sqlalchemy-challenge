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

# home--List all routes that are available.
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# precipitation--Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
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

# stations--Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

# tobs--Query the dates and temperature observations of the most active station for the last year of data.
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


# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>")
def start_only(start):
    session = Session(engine)
    
    for date in start:
        low_temp = session.query(func.min(Measurement.tobs)).filter(
            Measurement.station == 'USC00519281').all()
        high_temp = session.query(func.max(Measurement.tobs)).filter(
            Measurement.station == 'USC00519281').all()
        mean_temp = session.query(func.avg(Measurement.tobs)).filter(
            Measurement.station == 'USC00519281').all()
    
    session.close()

    = list(np.ravel(last_year_tobs))

    return jsonify()

# debug
if __name__ == '__main__':
    app.run(debug=True)
