"""Tests.classes.test_single module for wtforglib package."""

from unittest import TestCase

from wtforglib.single import singleton

# create two test classes decorated with the singleton

StdArg = bool | int | str


@singleton
class Foo:
    """A test class decorated with singleton"""


@singleton
class Bar:
    """A test class decorated with singleton"""

    arg: StdArg
    kwarg: StdArg

    def __init__(self, *args: StdArg, **kwargs: StdArg) -> None:
        self.arg = args[0]
        self.kwarg = kwargs.get("kwarg", "wtf")


class TestSingletonIntegration(TestCase):
    """Tests the singleton decorator in work"""

    def test_create_two_objects_from_same_class(self) -> None:
        """
        Checks whether an instantiation of decorated class
        returns the same object each time
        """
        self.assertEqual(Foo(), Foo())

    def test_create_two_objects_from_same_class_diff_args(self) -> None:
        """
        Checks whether an instantiation of decorated class
        returns the same object each time and its attributes
        does not change
        """
        # create an object
        bar1 = Bar(1, kwarg="foo")
        # check whether the object has attributes arg=1 kwarg=foo
        self.assertEqual(bar1.arg, 1)
        self.assertEqual(bar1.kwarg, "foo")
        # create another object
        bar2 = Bar(2, kwarg="bar")
        # check whether it's the same object
        self.assertEqual(bar1, bar2)
        # check whether its attributes are the same
        self.assertEqual(bar2.arg, 1)
        self.assertEqual(bar2.kwarg, "foo")

    # def test_two_objects_from_different_classes(self) -> None:
    #     """
    #     Checks whether an instantiations of different decorated classes
    #     return different objects
    #     """
    #     # create two objects from different decorated classes
    #     foo = Foo()
    #     bar = Bar(1, kwarg="bar")
    #     # check whether the objects are different
    #     self.assertNotEqual(foo, bar)

    # def test_wrapped_attribute(self):
    #     """
    #     Checks whether the __wrapped__ attribute contains a decorated class
    #     """
    #     # create an object from decorated class
    #     foo = Foo()
    #     # check whether the __wrapped__ attribute contains
    #     # a class of the foo object
    #     self.assertEqual(Foo.__wrapped__, foo.__class__)
