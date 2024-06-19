# Pytest soft asserts.

![PyPI](https://img.shields.io/pypi/v/nrt-pytest-soft-asserts?color=blueviolet&style=plastic)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nrt-pytest-soft-asserts?color=greens&style=plastic)
![PyPI - License](https://img.shields.io/pypi/l/nrt-pytest-soft-asserts?color=blue&style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dd/nrt-pytest-soft-asserts?style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nrt-pytest-soft-asserts?color=yellow&style=plastic)
[![Coverage Status](https://coveralls.io/repos/github/etuzon/python-nrt-pytest-soft-asserts/badge.svg)](https://coveralls.io/github/etuzon/pytohn-nrt-pytest-soft-asserts)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/etuzon/python-nrt-pytest-soft-asserts?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/etuzon/python-nrt-pytest-soft-asserts?style=plastic)
[![DeepSource](https://app.deepsource.com/gh/etuzon/python-nrt-pytest-soft-asserts.svg/?label=active+issues&token=d3XBT3-sw5yOtGTGWIJMpmT_)](https://app.deepsource.com/gh/etuzon/python-nrt-pytest-soft-asserts/?ref=repository-badge)

### Supported asserts:

| Assert                                                      | Description                                                                                 | Example                                                                                                         | Return                                             |
|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| assert_true(condition, message=None)                        | Verify that condition is True                                                               | soft_asserts.assert_true(a == b)                                                                                | True if assertion passes, False if assertion fails |
| assert_false(condition, message=None)                       | Verify that condition is False                                                              | soft_asserts.assert_false(a == b)                                                                               | True if assertion passes, False if assertion fails |
| assert_equal(first, second, message=None)                   | Verify that first is equal to second                                                        | soft_asserts.assert_equal(a, b)                                                                                 | True if assertion passes, False if assertion fails |
| assert_not_equal(first, second, message=None)               | Verify that first is not equal to second                                                    | soft_asserts.assert_not_equal(a, b)                                                                             | True if assertion passes, False if assertion fails |
| assert_is(first, second, message=None)                      | Verify that first and second are the same object                                            | soft_asserts.assert_is(a, b)                                                                                    | True if assertion passes, False if assertion fails |
| assert_is_not(first, second, message=None)                  | Verify that first and second are not the same object                                        | soft_asserts.assert_is_not(a, b)                                                                                | True if assertion passes, False if assertion fails |
| assert_is_none(obj, message=None)                           | Verify that obj is None                                                                     | soft_asserts.assert_is_none(a)                                                                                  | True if assertion passes, False if assertion fails |
| assert_is_not_none(obj, message=None)                       | Verify that obj is not None                                                                 | soft_asserts.assert_is_not_none(a)                                                                              | True if assertion passes, False if assertion fails |
| assert_in(obj, container, message=None)                     | Verify that obj is in container                                                             | soft_asserts.assert_in(a, [a, b, c])                                                                            | True if assertion passes, False if assertion fails |
| assert_not_in(obj, container, message=None)                 | Verify that obj is not in container                                                         | soft_asserts.assert_not_in(a, [b, c])                                                                           | True if assertion passes, False if assertion fails |
| assert_is_instance(obj, cls, message=None)                  | Verify that obj is instance of cls                                                          | soft_asserts.assert_is_instance(a, A)                                                                           | True if assertion passes, False if assertion fails |
| assert_is_not_instance(obj, cls, message=None)              | Verify that obj is not instance of cls                                                      | soft_asserts.assert_is_not_instance(a, B)                                                                       | True if assertion passes, False if assertion fails |
| assert_almost_equal(first, second, delta, message=None)     | Verify that first is almost equal to second<br/>and the different is equal or less to delta | soft_asserts.assert_almost_equal(1.001, 1.002, 0.1)                                                             | True if assertion passes, False if assertion fails |
| assert_not_almost_equal(first, second, delta, message=None) | Verify that first is not almost equal to second<br/>and the different is more than delta    | soft_asserts.assert_not_almost_equal(1.001, 1.002, 0.00001)                                                     | True if assertion passes, False if assertion fails |
| assert_raises(exception, method: Callable, *args, **kwargs) | Verify that method execution raise exception                                                | soft_asserts.assert_raises(TypeError, sum, 'a', 2)                                                              | True if assertion passes, False if assertion fails |
| assert_raises_with(exception, message=None)                 | Verify that execution in 'with' block raise exception                                       | with soft_asserts.assert_raised_with(ValueError):<br/>&nbsp;&nbsp;&nbsp;&nbsp;raise ValueError(ERROR_MESSAGE_1) |                                                    |
                                                                                                                                                        

In the end of each test, the soft asserts will be verified and the test will be marked as failed if any of the asserts failed.<br/>
To verify the soft asserts in the middle of the test, call `soft_asserts.assert_all()`.<br/>
<br/>
assert_all() will raise _AssertionError_ if any of the asserts failed.

<br/>
#### Steps

Each testing section can be divided to steps.<br/>
The meaning of this is that if one of the asserts in a step failed,<br/>
then the step will be entered to list of failure steps and next test can be skipped<br/>
if it is depended on the failed step.<br/> 

Example:

To make test be skipped if step failed, a custom marker should be created.

This is an example of such custom marker, but user can create its own custom marker.

In conftest.py file:

```python
import pytest


@pytest.fixture(autouse=True)
def run_before_test(request):
    markers = request.node.own_markers

    for marker in markers:
        if marker.name == 'soft_asserts':
            marker_params = marker.kwargs
            soft_asserts = marker_params['soft_asserts']
            skip_steps = marker_params['skip_steps']

            for step in skip_steps:
                if soft_asserts.is_step_in_failure_steps(step):
                    pytest.skip(f'Skipped because [{step}] failed.')
```

```python
import pytest
from nrt_pytest_soft_asserts.soft_asserts import SoftAsserts

soft_asserts = SoftAsserts()

STEP_1 = 'step_1'
STEP_2 = 'step_2'

def test_assert_with_steps():
    soft_asserts.set_step(STEP_1)
    # result is False
    result = soft_asserts.assert_true(False)
    # print False
    print(result)    
    soft_asserts.set_step(STEP_2) 
    soft_asserts.assert_true(False)
    
    # From this code section steps will not be attached to failure asserts
    soft_asserts.unset_step()
    soft_asserts.assert_true(False)
    
    soft_asserts.assert_all()


@pytest.mark.soft_asserts(soft_asserts=soft_asserts, skip_steps=[STEP_1])
def test_skip_if_step_1_fail():
    soft_asserts.assert_true(True)

@pytest.mark.soft_asserts(soft_asserts=soft_asserts, skip_steps=[STEP_2])
def test_skip_if_step_2_fail():
    soft_asserts.assert_true(True)
```

#### Print error on each failed assert

Each assertion failure can be printed.<br/>
This can be done by adding logger or by adding a print method.<br/><br/>

In case a logger will be added to soft asserts, then logger.error(message) will be used.<br/>

In case a print method will be added to soft asserts, then print_method(message) will be used.<br/></br>

_logger and print method cannot be added together._<br/><br/>

#### logger example:

```python
import logging
from nrt_pytest_soft_asserts.soft_asserts import SoftAsserts


logger = logging.getLogger('test')

soft_asserts = SoftAsserts()

# logger will be used to print message after each assert fail.
soft_asserts.set_logger(logger)


def test_assert_true_fail():
    i = 1
    j = 2
    # logger.error() will print messages to console for each assert that fails
    soft_asserts.assert_true(i + j == 5)
    # f'{i} is different from {j}' will be printed by logger.error() after assert will fail
    soft_asserts.assert_equal(i, j, f'{i} is different from {j}')
    soft_asserts.assert_all()
```

#### print method example:

```python
from nrt_pytest_soft_asserts.soft_asserts import SoftAsserts

def print_method(message):
    print(message)

soft_asserts = SoftAsserts()

# print_method will be used to print message after each assert fail.
soft_asserts.set_print_method(print_method)


def test_assert_true_fail():
    i = 1
    j = 2
    # print_method will print messages to console for each assert that fails
    soft_asserts.assert_true(i + j == 5)
    # f'{i} is different from {j}' will be printed by print_method after assert will fail
    soft_asserts.assert_equal(i, j, f'{i} is different from {j}')
    soft_asserts.assert_all()
```

Wiki: https://github.com/etuzon/python-nrt-pytest-soft-asserts/wiki