from enum import Enum
import math

def recruite_workers(workers, recruitment_count):
    recruited_workers = []
    sorted_workers = sorted(workers.values(), key = lambda worker: get_sorting_value(worker), reverse=True)
    
    current_count = 0
    for worker in sorted_workers:
        if(is_recruitable(worker)):
            print("Recruited worker {}".format(worker["ID"]))
            recruited_workers.append(worker)
            current_count += 1

            if(current_count >= recruitment_count):
                return recruited_workers
    return recruited_workers


def get_sorting_value(worker):
    if(worker["state"] == "CHARGING"):
        return math.inf
    else:
        print("Worker {} with battery level: {}".format(worker["ID"],worker["battery"]))
        return int(worker["battery"])


def is_recruitable(worker):
    return worker["available"] and worker["state"] != "SLEEPING"