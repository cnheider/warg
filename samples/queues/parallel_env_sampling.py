#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 01/08/2020
           """

import random
import time
from multiprocessing import Process, Queue, current_process, freeze_support


def worker(input, output):
    for func, args in iter(input.get, "STOP"):
        result = calculate(func, args)
        output.put(result)


def calculate(func, args):
    result = func(*args)
    return f"{current_process().name} says that {func.__name__}{args} = {result}"


def mul(a, b):
    time.sleep(0.5 * random.random())
    return a * b


def plus(a, b):
    time.sleep(0.5 * random.random())
    return a + b


def test():
    NUMBER_OF_PROCESSES = 4
    TASKS1 = [(mul, (i, 7)) for i in range(20)]
    TASKS2 = [(plus, (i, 8)) for i in range(10)]

    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    for task in TASKS1:  # Submit tasks
        task_queue.put(task)

    for i in range(NUMBER_OF_PROCESSES):  # Start worker processes
        Process(target=worker, args=(task_queue, done_queue)).start()

    print("Unordered results:")
    for i in range(len(TASKS1)):  # Get and print results
        print("\t", done_queue.get())

    for task in TASKS2:  # Add more tasks using `put()`
        task_queue.put(task)

    for i in range(len(TASKS2)):  # Get and print some more results
        print("\t", done_queue.get())

    for i in range(NUMBER_OF_PROCESSES):  # Tell child processes to stop
        task_queue.put("STOP")


if __name__ == "__main__":
    freeze_support()
    test()
