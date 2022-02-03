import urllib.request
import requests
import os
from sensor import load_sensor_data
from sensor import convert_data_to_tensor
import threading
import traceback
from status import uses_battery, get_status
import syft
import asyncio
from worker_with_model import WorkerWithModel
import torch
import signal
import sys

DATA_STREAM_SIMULATION_INTERVAL = 1
CONTROLLER_URL = os.getenv('CONTROLLER_URL', "http://localhost:5000")
remote_worker = None
isStopped = False
data_stream_thread = None
status_thread = None

@uses_battery
def status():
    try:
        r = requests.post(CONTROLLER_URL + "/status", data = {**get_status(), **get_worker_config()})
        print(r)
    except:
        traceback.print_exc()
        print("Error during status update")
    print(get_status())


def start_websocket_worker():
    global remote_worker
    asyncio.set_event_loop(asyncio.new_event_loop())
    try:
        config = get_worker_config()
        hook = syft.TorchHook(torch, is_client=True)
        remote_worker = WorkerWithModel(
            host=config['host'],
            hook=hook,
            id=config['ID'],
            port=config['port'])

        # initial data load on remote worker
        load_data_on_remote_worker()

        remote_worker.start()
        print('Websocket server started')
    except:
        print('Websocket server could not be started, check the configuration parameters')


def start_websocket_worker_thread():
    websocket_thread = threading.Thread(target=start_websocket_worker)
    websocket_thread.start()

def start_status_periodically():
    status_thread = threading.Thread(target=send_status_periodically)
    status_thread.start()

def send_status_periodically():
    e = threading.Event()
    while not e.wait(5) and not isStopped:
        status()

def start_stream_data_simulation():
    data_stream_thread = threading.Thread(target=send_new_data_to_websocket)
    data_stream_thread.start()

def send_new_data_to_websocket():
    print('Simulating stream of new data')
    e = threading.Event()
    while not e.wait(DATA_STREAM_SIMULATION_INTERVAL) and not isStopped:
        if remote_worker is not None:
            load_data_on_remote_worker()


def get_worker_id():
    try:
        worker_id = int(os.environ['WORKER_ID'])
    except:
        print('Worker id must be an integer, assigning default worker id')
        worker_id = 1
    return worker_id


def get_worker_config():
    config = {}
    try:
        config = {
            "ID": get_worker_id(),
            "host": os.environ['HOST'],
            "port": int(os.environ['PORT'])
        }
    except:
        print("Check docker-compose for worker configuration parameters")
    return config

def signal_handler(sig, frame):
    print('Shutting down worker')
    global isStopped, data_stream_thread
    isStopped = False

    if data_stream_thread is not None:
        data_stream_thread.join()

    if status_thread is not None:
        status_thread.join()

    sys.exit(0)

def load_data_on_remote_worker():
    remote_worker.clear_objects()
    tensor_X, tensor_y = convert_data_to_tensor(load_sensor_data(get_worker_id()))
    remote_worker.observations = tensor_X
    remote_worker.target = tensor_y

start_status_periodically()
start_websocket_worker()
start_stream_data_simulation()
signal.signal(signal.SIGINT, signal_handler)