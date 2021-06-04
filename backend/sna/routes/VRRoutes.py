import datetime
from flask import current_app as app
from flask import request, jsonify, escape, Response
from sna.helper.VRClassifier import VRClassifier
from sna.helper.encoder import JSONEncoder
from sna.db.Mongo import Database as MongoDB
from flask_cors import cross_origin
import json


db = MongoDB()
classifier = VRClassifier()
vr_dump = 'VR_dump'
collection = 'reporting_data'

@cross_origin
@app.route('/vr/list_report')
def list_report():
    db.initialize(vr_dump)
    data = db.aggregate(collection)
    return Response(json.dumps({'result': list(data)}, cls=JSONEncoder), mimetype='application/json')

@cross_origin
@app.route('/vr/input_report', methods=['POST'])
def input_report():
    db.initialize(vr_dump)
    datelog = str(datetime.datetime.now())
    nik = request.form['nik']
    vt = request.form['violence_type']
    rel = request.form['relation']
    vic = request.form['victim_age']
    ag = request.form['agressor_age']
    par = request.form['previous_abuse_report']
    lt = request.form['living_together']
    sc = request.form['short_chronology']
    report = [(rel, vic, ag, par, lt)]

    encoded_report = classifier.encode(report)
    scaled_report = classifier.scale(encoded_report)
    risk_level = classifier.predict(scaled_report)
    data = {
        'date_log': datelog,
        'nik' : nik,
        'violence_type': vt,
        'relation': rel,
        'victim_age': vic,
        'agressor_age': ag,
        'prev_abuse_report': par,
        'living_together': lt,
        'short_chronology': sc,
        'risk_level': risk_level
    }

    db.insert(collection, data)
    return Response(json.dumps({'result': list(data)}, cls=JSONEncoder), mimetype='application/json')
