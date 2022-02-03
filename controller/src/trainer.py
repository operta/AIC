import datetime
from threading import Timer
from recruitment import recruite_workers
import syft
import torch
from syft.workers.websocket_client import WebsocketClientWorker
from syft import PointerTensor
from torch import nn
import traceback

MIN_TRAINING_PERIOD_INTERVAL_IN_SECONDS = 15
WORKER_COUNT_FOR_TRAINING = 4

# Training parameters
hook = syft.TorchHook(torch, is_client=False)
me = hook.local_worker
me.is_client_worker=False
NUMBER_OF_INPUT_FEATURES = 5
NUMBER_OF_OUTPUT_FEATURES = 1
LEARNING_RATE = 0.00001
EPOCHS = 1
model = nn.Linear(NUMBER_OF_INPUT_FEATURES, NUMBER_OF_OUTPUT_FEATURES)
weights, bias = list(model.parameters())
isStopped = 0
timer = None
# records loss for every training round
average_epoch_loss = []

def start_periodical_training(workers):
    print('PERIODICAL TRAINING START')
    global timer
    if timer is not None:
        timer.cancel()
        timer = None

    now = datetime.datetime.now()

    run_training_on_workers(workers)

    global isStopped
    if isStopped == 1:
        print('Process stopped, don\'t run another training')
        return

    seconds_passed = get_seconds_passed(now)
    re_run_training_on_workers(seconds_passed, workers)

def stop_periodical_training():
    global isStopped
    global timer

    isStopped = 1
    if timer is not None:
        timer.cancel()

def close_connections(worker_pointers):
    for worker in worker_pointers:
        worker.close()

def run_training_on_workers(workers):
    global weights
    global bias
    global average_epoch_loss

    recruited = recruite_workers(workers, WORKER_COUNT_FOR_TRAINING)

    worker_pointers = []
    me.clear_objects()
    for worker in recruited:
        pointer = establish_web_socket_connection(worker)
        if pointer is not None:
            worker_pointers.append(pointer)

    no_of_workers = len(worker_pointers)

    if no_of_workers > 0:
        print("Training round started")
        for iter in range(EPOCHS):
            workers_loss = []
            for worker_pointer in worker_pointers:

                worker_pointer._send_msg_and_deserialize(command_name='load_model', weights=weights, bias=bias)
                worker_pointer._send_msg_and_deserialize(command_name='reset_gradients')
                loss = worker_pointer._send_msg_and_deserialize(command_name='predict')
                workers_loss.append(loss)
                worker_pointer._send_msg_and_deserialize(command_name='adjust_weights', learning_rate=LEARNING_RATE)

            worker_weights_sum, worker_bias_sum = sum_worker_weights_and_bias(worker_pointers)
            weights = torch.div(worker_weights_sum,no_of_workers)
            bias = torch.div(worker_bias_sum,no_of_workers)

            average_loss = round(sum(workers_loss) / no_of_workers, 2)
            average_epoch_loss.append(average_loss)

        close_connections(worker_pointers)
        print("Training round finished")
    else:
        print("No recruited workers for trainings")

# please provide array of pollutant measurements as input, for example [0.438731,10.85511,22.182,55.539261,35.708588]
def make_prediction(input):
    input_tensor = torch.tensor(input)
    output = input_tensor @ weights.t() + bias
    return round(output.item(), 2)

def sum_worker_weights_and_bias(worker_pointers):
    all_workers_weights = []
    all_workers_bias = []
    for wp in worker_pointers:
        all_workers_weights.append(PointerTensor(wp, 'weights').get())
        all_workers_bias.append(PointerTensor(wp, 'bias').get())
    worker_weights_sum = torch.sum(torch.stack(all_workers_weights), dim=0)
    worker_bias_sum = torch.sum(torch.stack(all_workers_bias), dim=0)
    return worker_weights_sum, worker_bias_sum


def establish_web_socket_connection(worker):
    remote_worker_pointer = None
    host = worker["host"]
    port = worker["port"]
    worker_id = worker["ID"]
    try:
        remote_worker_pointer = WebsocketClientWorker(
            host=host,
            hook=hook,
            id=worker_id,
            is_client_worker=True,
            verbose=True,
            port=port)
        # we add the worker to the list of known workers
        me.add_worker(remote_worker_pointer)
    except:
        print('Could not establish web socket connection to worker: ' + worker_id + " -> " + host + ":" + port, 500)
    return remote_worker_pointer


def re_run_training_on_workers(seconds_passed_since_last_training, workers):
    if(is_min_training_period_interval_passed(seconds_passed_since_last_training)):
        start_periodical_training(workers)
    else:
        seconds_to_min_interval = MIN_TRAINING_PERIOD_INTERVAL_IN_SECONDS - seconds_passed_since_last_training

        global timer
        timer = Timer(seconds_to_min_interval, start_periodical_training, args=[workers])
        timer.start()

def get_seconds_passed(since):
    return (datetime.datetime.now() - since).seconds

def is_min_training_period_interval_passed(seconds_passed):
    return seconds_passed > MIN_TRAINING_PERIOD_INTERVAL_IN_SECONDS

def get_loss():
    return average_epoch_loss