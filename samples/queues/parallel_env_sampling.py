#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 01/08/2020
           """

import random
import time
from multiprocessing import Process, Queue, current_process, freeze_support
from typing import Sequence


def worker(i: Queue, output: Queue) -> None:
    """
    task_queue
    done_queue

    """
    for func, args in iter(i.get, "STOP"):
        result = calculate(func, args)
        output.put(result)


def calculate(func: callable, args: Sequence) -> str:
    """description"""
    result = func(*args)
    return f"{current_process().name} says that {func.__name__}{args} = {result}"


def mul(a, b):
    """description"""
    time.sleep(0.5 * random.random())
    return a * b


def plus(a, b):
    """description"""
    time.sleep(0.5 * random.random())
    return a + b


def stest():
    number_of_processes = 4
    tasks1 = [(mul, (i, 7)) for i in range(20)]
    tasks2 = [(plus, (i, 8)) for i in range(10)]

    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    for task in tasks1:  # Submit tasks
        task_queue.put(task)

    for i in range(number_of_processes):  # Start worker processes
        Process(target=worker, args=(task_queue, done_queue)).start()

    print("Unordered results:")
    for i in range(len(tasks1)):  # Get and print results
        print("\t", done_queue.get())

    for task in tasks2:  # Add more tasks using `put()`
        task_queue.put(task)

    for i in range(len(tasks2)):  # Get and print some more results
        print("\t", done_queue.get())

    for i in range(number_of_processes):  # Tell child processes to stop
        task_queue.put("STOP")


if __name__ == "__main__":
    freeze_support()
    stest()
