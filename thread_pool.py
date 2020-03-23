from datetime import datetime
import random
from typing import *
import threading


def distribute_tasks(tasks : Iterable, groups : int):
    task_sets = [[] for _ in range(groups)]

    container_id = 0

    for task_id, task in enumerate(tasks):
        task_sets[container_id].append(task)
        container_id += 1
        if container_id == len(task_sets):
            container_id = 0
    return task_sets

def thread_solve(task_sets : List[list], thread_type : Type, *thread_args) -> None:
    """
    Thread object must have constructor, that takes task parameters, id and other thread_args given as function parameters
    """
    threads = [thread_type(task_sets[i], i, *thread_args) for i in range(len(task_sets))]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


controllers_tasks_performed = 0
controllers_target_tasks = 0
controllers_update_probability : float

controllers_time_start : datetime
controllers_last_update_time : datetime = None

controllers_beta = 0.95 # For exponentially moving average
controllers_current_avr = 0


class loading_controller:
    @staticmethod
    def init(target_tasks : int, update_probability : float):
        global controllers_target_tasks, controllers_update_probability, controllers_time_start
        controllers_target_tasks = target_tasks
        controllers_update_probability = update_probability
        controllers_time_start = datetime.now()

    @staticmethod
    def update():
        global controllers_tasks_performed, controllers_current_avr, controllers_last_update_time
        controllers_tasks_performed += 1
        if random.random() < controllers_update_probability:
            current_percent = 100 * controllers_tasks_performed / controllers_target_tasks
            percent_left = 100. - current_percent
            now = datetime.now()
            time_now = (now - controllers_time_start).total_seconds()
            speed = current_percent / time_now # Percents per second
            # local_speed = 1 / (now - controllers_last_update_time).total_seconds() if controllers_last_update_time is not None else speed
            # print("Local spreed:", local_speed)
            # controllers_current_avr += controllers_beta * (local_speed - controllers_current_avr)
            # controllers_last_update_time = now
            # short_term_speed = controller
            time_left_seconds = percent_left / speed
            speed_tasks_per_second = controllers_tasks_performed / time_now
            print(f"Task Controller: {controllers_tasks_performed} tasks performed of {controllers_target_tasks} ({round(current_percent, 4)} %), \t\t\
            long-term speed: {round(speed_tasks_per_second, 4)} tasks per second\t\t short-term speed: {round(controllers_current_avr, 4)}\
             time left: {round(time_left_seconds / 60, 4)} minutes")






