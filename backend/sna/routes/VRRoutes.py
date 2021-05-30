import datetime
from flask import request, jsonify, escape, Response
from sna.helper.VRClassifier import VRClassifier
from snahelper.encoder import JSONEncoder
from sna.db.Mongo import Database as MongoDB
from flask_cors import cross_origin
from flask import current_app as app

db = MongoDB()
classifier = VRClassifier()
vr_dump = 'VR_dump'
collection = 'reporting_data'
db.initialize(vr_dump)

@cross_origin
@app.routes('/vr/list_report')
def list_report():
    data = db.aggregate(collection)
    return Response(json.dumps({'result': list(data)}, cls=JSONEncoder), mimetype='application/json')

@cross_origin
@app.routes('/vr/input_report')
def input_report():
    datelog = str(datetime.datetime.now())
    nik = request.args['nik']
    vt = request.args['violence_type']
    rel = request.args['relation']
    vic = request.args['victim_age']
    ag = request.args['agressor_age']
    par = request.args['previous_abuse_report']
    lt = request.args['living_together']
    sc = request.args['short_chronology']
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
    db.insert_many(collection, data)
    return Response(json.dumps({'result': list(data)}, cls=JSONEncoder), mimetype='application/json')
