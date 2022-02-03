from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import random
import datetime
import threading
import traceback
from trainer import start_periodical_training
from trainer import stop_periodical_training
from trainer import run_training_on_workers
from trainer import get_loss
from trainer import make_prediction
import signal
import sys
import logging



app = Flask(__name__)
CORS(app, resources=r'/api/*')
app.config['CORS_HEADERS'] = 'Content-Type'

jobs = []
workers = {}
workers_lock = threading.Lock()
MIN_STATUS_UPDATE_INTERVAL_SEC = 7
training_thread = None


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/status', methods=['POST'])
def status():
    try:
        worker_id = register(request.form["ID"])
        update_status(worker_id, request.form)
        worker = workers[worker_id]
        return "OK"
    except:
        traceback.print_exc()
        return "Error during initialization or update of status", 500

@app.route('/api/status', methods=['GET'])
def getStatus():
    return workers

@app.route('/api/losses', methods=['GET'])
def get_losses():
    return jsonify({"loss": get_loss()})

@app.route('/api/jobs', methods=['GET'])
def getJobs():
    return jsonify(jobs)

@app.route('/api/predict', methods=['POST','OPTIONS'])
def create_task():
    if request.method == "OPTIONS": # CORS preflight
        return build_cors_preflight_response()
    elif not request.json or not 'datetime' in request.json:
        abort(400)
    else:
        result = make_prediction([
        request.json['co'],
        request.json['no2'],
        request.json['o3'],
        request.json['pm10'],
        request.json['pm2_5']])
 
        prediction_request = {
        'datetime': request.json['datetime'],
        'co': request.json['co'],
        'no2': request.json['no2'],
        'o3': request.json['o3'],
        'pm10': request.json['pm10'],
        'pm2_5': request.json['pm2_5'],
        'result': result,
        'completed': False
        }
        jobs.append(prediction_request)  
        return jsonify({'prediction_request': prediction_request}) , 201

def build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "POST")
    return response

def corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def register(id):
    workers_lock.acquire()

    if(not id in workers):
        workers[id] = {}

    workers_lock.release()
    return id


def update_status(worker_key, data):
    workers_lock.acquire()

    for key in data:
        workers[worker_key][key] = data[key]
    workers[worker_key]["last_update"] = datetime.datetime.now()
    workers[worker_key]["available"] = True

    workers_lock.release()


def start_status_checker():
    checker_thread = threading.Thread(target=check_status_update_periodically, daemon=True)
    checker_thread.start()


def start_training():
    print('TRAINIG STARTED')
    training_thread = threading.Thread(target=start_periodical_training, args=[workers])
    training_thread.start()


def check_status_update_periodically():
    e = threading.Event()
    while not e.wait(MIN_STATUS_UPDATE_INTERVAL_SEC):
        set_availability_regaring_to_status_update()


def set_availability_regaring_to_status_update():
    workers_lock.acquire()

    for worker_id in workers:
        if(not status_updated_recently(workers[worker_id])):
            workers[worker_id]["available"] = False

    workers_lock.release()


def status_updated_recently(worker):
    diff = datetime.datetime.now() - worker["last_update"]
    return diff.seconds < MIN_STATUS_UPDATE_INTERVAL_SEC


def signal_handler(sig, frame):
    print('Shutting down controller')
    stop_periodical_training()

    if training_thread is not None:
        training_thread.join()

    sys.exit(0)


if __name__ == '__main__':
    start_training()
    start_status_checker()

    signal.signal(signal.SIGINT, signal_handler)

    app.run(host='0.0.0.0')
