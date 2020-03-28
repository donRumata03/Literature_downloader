from datetime import datetime, timedelta
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

controllers_prev_times = [] # For averages
controllers_gate_width : int = 0

class loading_controller:
    @staticmethod
    def init(target_tasks : int, update_probability : float, gate_width : int = 200):
        global controllers_target_tasks, controllers_update_probability, controllers_time_start, controllers_gate_width
        controllers_target_tasks = target_tasks
        controllers_update_probability = update_probability
        controllers_gate_width = gate_width
        controllers_time_start = datetime.now()

    @staticmethod
    def update():
        global controllers_tasks_performed, controllers_last_update_time, controllers_prev_times
        controllers_tasks_performed += 1
        if random.random() < controllers_update_probability:
            current_percent = 100 * controllers_tasks_performed / controllers_target_tasks
            percent_left = 100. - current_percent
            now = datetime.now()
            time_now = (now - controllers_time_start).total_seconds()
            controllers_prev_times.append(time_now)
            if len(controllers_prev_times) > controllers_gate_width + 1:
                prev_moment = controllers_prev_times[-controllers_gate_width]
                local_speed = (time_now - prev_moment) / controllers_gate_width
                print("Local speed :", local_speed)
            speed = current_percent / time_now # Percents per second
            # local_speed = 1 / (now - controllers_last_update_time).total_seconds() if controllers_last_update_time is not None else speed
            # print("Local spreed:", local_speed)
            # controllers_current_avr += controllers_beta * (local_speed - controllers_current_avr)
            # controllers_last_update_time = now
            # short_term_speed = controller
            time_left_seconds = percent_left / speed
            time_left_minutes = time_left_seconds / 60
            speed_tasks_per_second = controllers_tasks_performed / time_now
            print(f"Task Controller: {controllers_tasks_performed} tasks performed of {controllers_target_tasks} ({round(current_percent, 4)} %), \t\t\
            long-term speed: {round(speed_tasks_per_second, 4)} tasks per second\t\t\
             time left: {round(time_left_minutes, 4)} minutes\t\ttime planning: {now + timedelta(minutes = time_left_minutes)}")






