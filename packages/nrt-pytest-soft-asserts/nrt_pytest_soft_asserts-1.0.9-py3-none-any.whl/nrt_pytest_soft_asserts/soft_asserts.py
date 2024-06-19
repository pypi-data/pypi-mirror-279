from dataclasses import dataclass
from typing import Callable, Optional, List


@dataclass
class Failure:
    error: str
    step: str


class SoftAsserts:
    """
    Soft asserts class.

    @author: Eyal Tuzon.
    """

    __failures: List[Failure] = []
    __logger = None
    __print_method: Optional[Callable] = None
    __current_step: Optional[str] = None
    __failure_steps: List[str] = []

    def __init__(self):
        self.__validate_params()
        self.__failures = []

    def set_step(self, step: str):
        self.__current_step = step

    def unset_step(self):
        self.__current_step = None

    def assert_true(self, condition, message=None) -> bool:
        if not condition:
            error = message or 'Expected True, got False.'
            self.__append_to_failures(error)
            return False

        return True

    def assert_false(self, condition, message=None) -> bool:
        if condition:
            error = message or 'Expected False, got True.'
            self.__append_to_failures(error)
            return False

        return True

    def assert_equal(self, first, second, message=None) -> bool:
        if first != second:
            error = message or f'{first} != {second}'
            self.__append_to_failures(error)
            return False

        return True

    def assert_not_equal(self, first, second, message=None) -> bool:
        if first == second:
            error = message or f'{first} == {second}'
            self.__append_to_failures(error)
            return False

        return True

    def assert_is(self, first, second, message=None) -> bool:
        if first is not second:
            error = message or f'{first} is not {second}'
            self.__append_to_failures(error)
            return False

        return True

    def assert_is_not(self, first, second, message=None) -> bool:
        if first is second:
            error = message or f'{first} is {second}'
            self.__append_to_failures(error)
            return False

        return True

    def assert_is_none(self, obj, message=None) -> bool:
        if obj is not None:
            error = message or f'{obj} is not None'
            self.__append_to_failures(error)
            return False

        return True

    def assert_is_not_none(self, obj, message=None) -> bool:
        if obj is None:
            error = message or 'obj is None'
            self.__append_to_failures(error)
            return False

        return True

    def assert_in(self, obj, container, message=None) -> bool:
        if obj not in container:
            error = message or f'{obj} not in {container}'
            self.__append_to_failures(error)
            return False

        return True

    def assert_not_in(self, obj, container, message=None) -> bool:
        if obj in container:
            error = message or f'{obj} in {container}'
            self.__append_to_failures(error)
            return False

        return True

    def assert_is_instance(self, obj, cls, message=None) -> bool:
        if not isinstance(obj, cls):
            error = message or f'{obj} is not instance of {cls}'
            self.__append_to_failures(error)
            return False

        return True

    def assert_not_is_instance(self, obj, cls, message=None) -> bool:
        if isinstance(obj, cls):
            error = message or f'{obj} is instance of {cls}'
            self.__append_to_failures(error)
            return False

        return True

    def assert_almost_equal(self, first, second, delta, message=None) -> bool:
        if not self.__is_almost_equal(first, second, delta):
            error = message or f'Assertion failed: {first} not almost equal to {second}'
            self.__append_to_failures(error)
            return False

        return True

    def assert_not_almost_equal(self, first, second, delta, message=None) -> bool:
        if self.__is_almost_equal(first, second, delta):
            error = message or f'Assertion failed: {first} almost equal to {second}'
            self.__append_to_failures(error)
            return False

        return True

    def assert_raises(self, exception, method: Callable, *args, **kwargs) -> bool:
        try:
            method(*args, **kwargs)
            error = f'{exception} not raised'
            self.__append_to_failures(error)
            return False
        except Exception as e:
            if not isinstance(e, exception):
                error = f'{e} is not instance of {exception}'
                self.__append_to_failures(error)
                return False

        return True

    def assert_raised_with(self, exception, message=None):
        class AssertRaises:
            __exception = None
            __append_to_failures: Callable = None

            def __init__(self, e, append_to_failures: Callable):
                self.__exception = e
                self.__append_to_failures = append_to_failures

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                if exc_type is None:
                    error = message or f'{self.__exception} not raised'
                    self.__append_to_failures(error)
                elif exc_type != self.__exception:
                    error = message or f'{exc_type} is not type of {self.__exception}'
                    self.__append_to_failures(error)

                return True

        return AssertRaises(exception, self.__append_to_failures)

    def assert_all(self):
        """
        Raises AssertionError if any of the asserts failed.
        :return:
        """

        self.unset_step()

        if self.failures:
            failures = self.failures.copy()
            self.__failures = []

            self.failure_steps = (
                list(dict.fromkeys(
                        [failure.step for failure in failures
                         if failure.step is not None])))

            raise AssertionError('\n'.join([failure.error for failure in failures]))

    def is_step_in_failure_steps(self, step: str) -> bool:
        return step in self.failure_steps

    def init_failure_steps(self):
        self.failure_steps = []

    @property
    def failures(self):
        return self.__failures

    @property
    def failure_steps(self):
        return self.__failure_steps

    @failure_steps.setter
    def failure_steps(self, value):
        self.__failure_steps = value

    def __append_to_failures(self, error):
        self.__failures.append(Failure(error, self.__current_step))
        self.__print_error_to_log(error)

    @classmethod
    def __print_error_to_log(cls, error):
        cls.__validate_params()

        if cls.__print_method:
            cls.__print_method(error)
        elif cls.__logger:
            cls.__logger.error(error)

    @classmethod
    def __validate_params(cls):
        if cls.__logger and cls.__print_method:
            raise ValueError('Cannot set both logger and print_method')

    @classmethod
    def __is_almost_equal(cls, first, second, delta):
        return abs(first - second) <= delta

    @classmethod
    def set_logger(cls, logger):
        cls.__logger = logger

    @classmethod
    def unset_logger(cls):
        cls.__logger = None

    @classmethod
    def set_print_method(cls, print_method: Callable):
        cls.__print_method = print_method

    @classmethod
    def unset_print_method(cls):
        cls.__print_method = None
