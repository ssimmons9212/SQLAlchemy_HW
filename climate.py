import sqlalchemy
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, url_for, render_template, request, redirect
import datetime as dt
import os 
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/samms/Desktop/SQLAlchemy_HW/upload_images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# <img src="{{ url_for('static', filename='img.png') }}">
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

# Base.classes.keys()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

filter_LastYear = dt.date(2017,8,23) - dt.timedelta(days = 365)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return "Hello"



@app.route("/api/v1.0/precipitation")
def prcp():

   
    prcp_list = []
    prcp_data = session.query(Measurement.date, Measurement.prcp, Measurement.station).filter(Measurement.date >= filter_LastYear).\
                order_by(Measurement.date).all()
    
    for data in prcp_data:
        prcp_dict = {}
        prcp_dict['date'] = data.date
        prcp_dict['prcp'] = data.prcp
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)


# @app.route('/upload')
# def upload_file():
#    return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['/Users/samms/Desktop/SQLAlchemy_HW/upload_images/figure.png']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

@app.route("/api/v1.0/stations")
def stat():
    results = session.query(Station.name).all()
    stations = list(results)
    return jsonify(stations)

    return "stations"
@app.route("/api/v1.0/temp4station")
def tobs():
    station_stats = session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    best_station = station_stats[0]
    station_results = session.query(Measurement.date, Measurement.tobs, Measurement.station).filter(Measurement.station == best_station, Measurement.date>=filter_LastYear).order_by(Measurement.date).all()
    station_rain = list(station_results)
    return jsonify(station_rain)
    

if __name__ == "__main__":
    app.run(debug=True)