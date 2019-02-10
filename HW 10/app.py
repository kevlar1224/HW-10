from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import pandas as pd



app = Flask(__name__)

@app.route("/")
def main():
    return (
        f"Available routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start and /api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    engine  = create_engine(f"sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    session = Session(engine)
    precip_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>"2016-08-23").all()
    date_tup, precip_tup = zip(*precip_data)
    precip_dict = {}
    for i in range(len(date_tup)):
        precip_dict[date_tup[i]] = precip_tup[i]
    return jsonify(precip_dict)

@app.route("/api/v1.0/station")
def station():
    engine  = create_engine(f"sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Station = Base.classes.station
    session = Session(engine)
    station_data = session.query(Station.station).all()
    station_tup = zip(*station_data)
    return jsonify(list(station_tup))

@app.route("/api/v1.0/tobs")
def temperatures():
    engine  = create_engine(f"sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    session = Session(engine)
    temp_data = session.query(Measurement.tobs).filter(Measurement.date>"2016-08-23").all()
    temp_tup = zip(*temp_data)
    return jsonify(list(temp_tup))

@app.route("/api/v1.0/<start>")
def start_only(start):
    engine  = create_engine(f"sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    session = Session(engine)
    temp_data = session.query(func.min(Measurement.tobs),\
        func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date > start).all()
    min_temp, max_temp, avg_temp = zip(*temp_data)
    return (f"Minimum temperature after start date: {min_temp[0]}<br/>"
    f"Maximum temperature after start date: {max_temp[0]}<br/>"
    f"Average temperature after start date: {round(float(avg_temp[0]),1)}<br/>")


@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start, end):
    engine  = create_engine(f"sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    session = Session(engine)
    temp_data = session.query(func.min(Measurement.tobs),\
        func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date > start, Measurement.date < end).all()
    min_temp, max_temp, avg_temp = zip(*temp_data)
    return (f"Minimum temperature after start date: {min_temp[0]}<br/>"
    f"Maximum temperature after start date: {max_temp[0]}<br/>"
    f"Average temperature after start date: {round(float(avg_temp[0]),1)}<br/>")


if __name__ == "__main__":
    app.run(debug=True)