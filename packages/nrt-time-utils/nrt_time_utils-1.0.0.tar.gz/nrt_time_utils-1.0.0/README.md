# Time Utilities

### Time utilities in Python.

![PyPI](https://img.shields.io/pypi/v/nrt-time-utils?color=blueviolet&style=plastic)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nrt-time-utils?color=greens&style=plastic)
![PyPI - License](https://img.shields.io/pypi/l/nrt-time-utils?color=blue&style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dd/nrt-time-utils?style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nrt-time-utils?color=yellow&style=plastic)
[![Coverage Status](https://coveralls.io/repos/github/etuzon/python-nrt-time-utils/badge.svg)](https://coveralls.io/github/etuzon/pytohn-nrt-time-utils)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/etuzon/python-nrt-time-utils?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/etuzon/python-nrt-time-utils?style=plastic)
[![DeepSource](https://app.deepsource.com/gh/etuzon/python-nrt-time-utils.svg/?label=active+issues&show_trend=false&token=eTDGJ29l60LGTuhQtl6DQqJG)](https://app.deepsource.com/gh/etuzon/python-nrt-time-utils/)

## TimeUtil class

### Methods

| **Method**                  | **Description**                                        | **Parameters**                                                                                                                                                       | **Returns**                                                       |
|-----------------------------|--------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| `date_ms_to_date_str`       | Converts a date in milliseconds to a date string.      | `date_ms (int)` The date in milliseconds to convert to a date string.<br>`format_str (str, Default: YMD_HMSF_DATE_FORMAT)` The format string to convert the date to. | `str` The date string.                                            |
| `date_ms_to_date_time`      | Converts a date in milliseconds to a date time object. | `date_ms (int)` The date in milliseconds to convert to a date time object.                                                                                           | `datetime` The date time object.                                  |
| `date_str_to_date_time`     | Converts a date string to a date time object.          | `date_str (str)` The date string to convert to a date time object.<br>`format_str (str, Default: YMD_HMSF_DATE_FORMAT)` The format string to convert the date to.    | `datetime` The date time object.                                  |
| `date_time_to_date_ms`      | Converts a date time object to a date in milliseconds. | `dt (datetime)` The date time object to convert to a date in milliseconds.                                                                                           | `int` The date in milliseconds.                                   |
| `get_current_date_ms`       | Returns the current date in milliseconds.              |                                                                                                                                                                      | `int` The current date in milliseconds.                           |
| `get_timezone_offset_hours` | Returns the timezone offset in hours.                  | `timezone_str (str)` A string representing the timezone                                                                                                              | `int` The timezone offset in hours.                               |
| `is_leap_year`              | Checks if a year is a leap year.                       | `year (int)` The year to check if it is a leap year.                                                                                                                 | `bool` True if the year is a leap year, False otherwise.          |
| `is_timeout_ms`             | Checks if a timeout in milliseconds has passed.        | `start_time_ms (int)` The start time in milliseconds.<br>`timeout_ms (int)` The timeout in milliseconds.                                                             | `bool` True if the timeout has passed, False otherwise.           |
| `is_date_in_format`         | Checks if a date string is in a specific format.       | `date_str (str)` The date string to check.<br>`format_str (str)` The format string to check.                                                                         | `bool` True if the date string is in the format, False otherwise. |

### Examples:

- #### TimeUtil.date_ms_to_date_str

    **Code**
    ```python
    from time_utils import TimeUtil

    # Convert a date in milliseconds to a date string
    date_str = TimeUtil.date_ms_to_date_str(1617223200000)

    print(date_str)
    ```
    **Output**
    ```
    2021-03-31 00:00:00.000
    ```

- #### TimeUtil.date_ms_to_date_time
        
    **Code**
    ```python
    from time_utils import TimeUtil

    # Convert a date in milliseconds to a date time object
    dt = TimeUtil.date_ms_to_date_time(1617223200000)

    print(dt)
    ```
    **Output**
    ```
    2021-03-31 00:00:00
    ```
  
- #### TimeUtil.date_str_to_date_time

    **Code**
    ```python
    from time_utils import TimeUtil

    # Convert a date string to a date time object
    dt = TimeUtil.date_str_to_date_time('2021-03-31 00:00:00.000')

    print(dt)
    ```
    **Output**
    ```
    2021-03-31 00:00:00
    ```

- #### TimeUtil.date_time_to_date_ms

    **Code**
    ```python
    from time_utils import TimeUtil
    from datetime import datetime

    # Convert a date time object to a date in milliseconds
    date_ms = TimeUtil.date_time_to_date_ms(datetime(2021, 3, 31, 0, 0, 0))

    print(date_ms)
    ```
    **Output**
    ```
    1617223200000
    ```
  
- #### TimeUtil.get_current_date_ms

    **Code**
    ```python
    from time_utils import TimeUtil

    # Get the current date in milliseconds
    current_date_ms = TimeUtil.get_current_date_ms()

    print(current_date_ms)
    ```
    **Output**
    ```
    1617223200000
    ```

- #### TimeUtil.get_timezone_offset_hours

    **Code**
    ```python
    from time_utils import TimeUtil

    # Get the timezone offset in hours
    timezone_offset = TimeUtil.get_timezone_offset_hours('PDT')

    print(timezone_offset)
    ```
    **Output**
    ```
    -7
    ```

- #### TimeUtil.is_leap_year

    **Code**
    ```python
    from time_utils import TimeUtil

    # Check if a year is a leap year
    is_leap_year = TimeUtil.is_leap_year(2020)

    print(is_leap_year)
    ```
    **Output**
    ```
    True
    ```
  
- #### TimeUtil.is_timeout_ms

    **Code**
    ```python
    from time_utils import TimeUtil
    from time import sleep

    current_date_ms = TimeUtil.get_current_date_ms()
    is_timeout = TimeUtil.is_timeout_ms(current_date_ms, 1000)
    print(is_timeout)
    sleep(2)
    is_timeout = TimeUtil.is_timeout_ms(current_date_ms, 1000)
    print(is_timeout)
    ```
    **Output**
    ```
    False
    True
    ```
  
- #### TimeUtil.is_date_in_format

    **Code**
    ```python
    from time_utils import TimeUtil
    from time_utils import YMD_HMSF_DATE_FORMAT

    # Check if a date string is in a specific format
    is_date_in_format = \
        TimeUtil.is_date_in_format('2021-03-31 00:00:00.000', YMD_HMSF_DATE_FORMAT)

    print(is_date_in_format)
    ```
    **Output**
    ```
    True
    ```