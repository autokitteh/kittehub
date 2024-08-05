"""Executable tasks that run in our workflow."""

from collections.abc import Callable


def task1() -> Callable | None:
    print("Task 1 is doing stuff...")
    return task2


def task2() -> Callable | None:
    print("Task 2 is doing stuff...")
    return task3


def task3() -> Callable | None:
    print("Task 3 is doing stuff...")
    raise RuntimeError("Something bad happened")


def task4() -> Callable | None:
    print("Task 4 is doing stuff...")
    return None  # This is the last task.
