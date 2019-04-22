#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from warg.pooled_queue_processor import PooledQueueProcessor, PooledQueueTask

__author__ = "cnheider"


class Square(PooledQueueTask):
    def call(self, i, *args, **kwargs):
        return i * 2


class Exc(PooledQueueTask):
    def call(self, *args, **kwargs):
        raise NotImplementedError


def identity(*args, **kwargs):
    return args, kwargs


@pytest.mark.slow
def test_integration_success():
    task = Square()

    with PooledQueueProcessor(task, [2], fill_at_construction=True, max_queue_size=10) as processor:
        for a, _ in zip(processor, range(30)):
            pass
            # print(a)


@pytest.mark.slow
def test_integration_func():
    task = identity

    with PooledQueueProcessor(task, [2], max_queue_size=10) as processor:
        for a, _ in zip(processor, range(30)):
            pass
            # print(a)


def test_lambda_func():
    task = lambda x: x

    with PooledQueueProcessor(task, [2], max_queue_size=10) as processor:
        for a, _ in zip(processor, range(30)):
            pass
            # print(a)


def test_integration_except():
    task = Exc()

    with pytest.raises(NotImplementedError) as exc_info:
        task()  # TODO: MP does not work in pytest
        processor = PooledQueueProcessor(task, [2], max_queue_size=10, blocking=True)
        for a, _ in zip(processor, range(30)):
            pass
            # print(a)

    assert exc_info.type is NotImplementedError


# @pytest.mark.slow
def test_integration_except_ctx():
    task = Exc()

    with pytest.raises(NotImplementedError) as exc_info:
        task()  # TODO: MP does not work in pytest
        with PooledQueueProcessor(task, [2], max_queue_size=10) as processor:
            for a, _ in zip(processor, range(30)):
                pass
                # print(a)

    assert exc_info.type is NotImplementedError


if __name__ == "__main__":
    test_lambda_func()
