"""Tests.classes.resettable module for wtforglib package."""

from threading import Event, Thread

from wtforglib.singles import r_singleton

# Example classes to apply the singleton decorators to

DEFAULT_VALUE = 42
TEST_VALUE = 24


@r_singleton
class ResettableSingleton:
    """ResettableSingleton class."""

    def __init__(self, valor=DEFAULT_VALUE) -> None:
        self.valor = valor


def test_regular_singleton_behavior():
    instance1 = ResettableSingleton()
    instance2 = ResettableSingleton()
    assert instance1 is instance2, "Both instances should be the same object"
    ResettableSingleton.reset()
    instance3 = ResettableSingleton(TEST_VALUE)
    assert instance1 is not instance3, "Both instances should be different objects"
    assert instance3.valor == TEST_VALUE


def test_regular_singleton_with_different_arguments():  # noqa: WPS118
    ResettableSingleton.reset()
    instance1 = ResettableSingleton()
    instance2 = ResettableSingleton(TEST_VALUE)
    assert (
        instance1 is instance2
    ), "Both instances should be the same object regardless of args"
    assert (
        instance2.valor == DEFAULT_VALUE
    ), "The valor should remain from the first instantiation"


def test_singleton_with_threading():
    event = Event()  # Can call
    event2 = Event()  # Can set Flag
    event3 = Event()  # Can exit

    class Flag:
        flag = False

    def get_instance_after_event():
        event.wait()
        Flag.flag = ResettableSingleton(False).valor
        event2.set()
        event3.wait()

    my_thread = Thread(target=get_instance_after_event)
    my_thread.start()

    assert ResettableSingleton(True).valor

    assert not Flag.flag

    event.set()
    event2.wait()
    assert Flag.flag
    event3.set()
    my_thread.join()

    assert Flag.flag
