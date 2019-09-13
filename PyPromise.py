from typing import Any, Callable
from threading import Thread
from enum import IntEnum


class state_enum(IntEnum):
    """Enum used for promise states"""
    pending = 0  # Pending
    rejected = 1  # Threw exception
    fulfilled = 2  # Completely finished
    settled = 3  # Exception handled


class Promise:
    """
    A spiritual port of JS promises, check __init__ for constructor arguments
    """

    def __init__(self, function: Callable[[], Any]):
        """
        Construct a Promise object from a Callable function.
            - function -> Callable that takes no parameters, returns anything.
        """
        self.__func = function
        self.__thread = None
        self.__then_f = None
        self.__catch_f = None
        self.__excepted = False
        self.__handled_exception = False

    def __del__(self):
        """
        Destructors that handles waiting for Promise to finish so thread can safely be destroyed
        """
        self.wait_for()

    def then(self, function: Callable[[], Any]) -> ("Reference to Promise"):
        """
        Set function that gets called after <function>, entered in constructor has been called and hasn't excepted.
            - function -> Callable that takes no parameters, returns anything.

        Will call Promise::start if both then() and catch() have been set
        """
        self.__then_f = function
        if not self.__catch_f:
            return self

        self.start()
        return self

    def catch(self, function: Callable[[BaseException], Any]) -> ("Reference to Promise"):
        """
        Set funciton that gets called incase an exception occurs in <function>, which has been entered in the constructor.
            - function -> Callable that takes a `BaseException`, returns anything.

        Will call Promise::start if both then() and catch() have been set
        """
        self.__catch_f = function
        if not self.__then_f:
            return self
        self.start()
        return self

    def start(self) -> ("Reference to Promise"):
        """
        Starts promise in background thread.
        This function will not have to be called if both .then() and .catch() have already been set.
        """
        self.__thread = Thread(target=self.__async_func)
        self.__thread.start()
        return self

    def wait_for(self) -> ("Reference to Promise"):
        """
        Waits for promise to finish.
        """
        try:
           self.__thread.join()
        except RuntimeError:
            return self
        return self

    def __async_func(self):
        try:
            self.__func()
        except BaseException as E:
            if not self.__catch_f:
                raise E
            self.__excepted = True
            self.__catch_f(E)
            self.__handled_exception = True
            return
        if not self.__then_f:
            return
        self.__then_f()

    @property
    def state(self) -> int:
        """
        Returns state of current Promise
        """
        if self.__thread.is_alive():
            if (self.__excepted and not self.__handled_exception):
                return state_enum.rejected
            elif (self.__excepted and self.__handled_exception):
                return state_enum.settled
            return state_enum.pending
        return state_enum.fulfilled


if __name__ == '__main__':
    def throw_error():
        raise RuntimeError("Test")

    Promise(lambda: throw_error) \
        .then(lambda: print("Succesfully finished")) \
        .catch(lambda x: print(f"An exception has occured: {x}"))

    Promise(lambda: print("Hello")) \
        .then(lambda: print("Finished")) \
        .catch(lambda x: print(x))
