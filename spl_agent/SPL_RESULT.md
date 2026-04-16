# SPL Report

## Project Overview

- project_name: datetime-utils
- source_type: git
- source: https://github.com/RhetTbull/datetime-utils
- commit: 5a1b82b5a7e392294ed9d9e3ad6832dd10233694
- module_count: 2
- function_count: 28

## Reading Guide

- 先看 `Module Index`，快速定位模块。
- 再看 `Function Index`，快速跳转到函数。
- 每个函数都提供可折叠的 SPL 代码块，减少滚动干扰。

## Module Index

- [datetime_tzutils.py](#module-datetime_tzutils-py) (9 functions)
- [test_datetime_tzutils.py](#module-test_datetime_tzutils-py) (19 functions)

## Function Index

### datetime_tzutils.py

- [datetime_has_tz](#fn-datetime_tzutils-py-datetime_has_tz)
- [datetime_naive_to_local](#fn-datetime_tzutils-py-datetime_naive_to_local)
- [datetime_naive_to_utc](#fn-datetime_tzutils-py-datetime_naive_to_utc)
- [datetime_remove_tz](#fn-datetime_tzutils-py-datetime_remove_tz)
- [datetime_to_new_tz](#fn-datetime_tzutils-py-datetime_to_new_tz)
- [datetime_tz_to_utc](#fn-datetime_tzutils-py-datetime_tz_to_utc)
- [datetime_utc_to_local](#fn-datetime_tzutils-py-datetime_utc_to_local)
- [get_local_tz](#fn-datetime_tzutils-py-get_local_tz)
- [utc_offset_seconds](#fn-datetime_tzutils-py-utc_offset_seconds)

### test_datetime_tzutils.py

- [test_datetime_has_tz](#fn-test_datetime_tzutils-py-test_datetime_has_tz)
- [test_datetime_naive_to_local](#fn-test_datetime_tzutils-py-test_datetime_naive_to_local)
- [test_datetime_naive_to_utc](#fn-test_datetime_tzutils-py-test_datetime_naive_to_utc)
- [test_datetime_remove_tz](#fn-test_datetime_tzutils-py-test_datetime_remove_tz)
- [test_datetime_to_new_tz](#fn-test_datetime_tzutils-py-test_datetime_to_new_tz)
- [test_datetime_to_new_tz_type_error](#fn-test_datetime_tzutils-py-test_datetime_to_new_tz_type_error)
- [test_datetime_to_new_tz_value_error](#fn-test_datetime_tzutils-py-test_datetime_to_new_tz_value_error)
- [test_datetime_tz_to_utc](#fn-test_datetime_tzutils-py-test_datetime_tz_to_utc)
- [test_datetime_tz_to_utc_dst](#fn-test_datetime_tzutils-py-test_datetime_tz_to_utc_dst)
- [test_datetime_utc_to_local](#fn-test_datetime_tzutils-py-test_datetime_utc_to_local)
- [test_datetime_utc_to_local_error_not_utc](#fn-test_datetime_tzutils-py-test_datetime_utc_to_local_error_not_utc)
- [test_get_local_tz](#fn-test_datetime_tzutils-py-test_get_local_tz)
- [test_get_local_tz_dst](#fn-test_datetime_tzutils-py-test_get_local_tz_dst)
- [test_get_local_tz_error](#fn-test_datetime_tzutils-py-test_get_local_tz_error)
- [test_not_datetime_has_tz](#fn-test_datetime_tzutils-py-test_not_datetime_has_tz)
- [test_type_error](#fn-test_datetime_tzutils-py-test_type_error)
- [test_utc_offset_seconds](#fn-test_datetime_tzutils-py-test_utc_offset_seconds)
- [test_value_error_naive](#fn-test_datetime_tzutils-py-test_value_error_naive)
- [test_value_error_not_naive](#fn-test_datetime_tzutils-py-test_value_error_not_naive)

## SPL Details

<a id="module-datetime_tzutils-py"></a>
### Module: datetime_tzutils.py

- function_count: 9

<a id="fn-datetime_tzutils-py-datetime_has_tz"></a>
#### Function: datetime_has_tz

- key: `datetime_tzutils.py::datetime_has_tz`
- spl_line_count: 23

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Return True if datetime dt has tzinfo else False" datetime_has_tz]
    [INPUTS]
        <REF> dt </REF>: datetime.datetime "Input parameter dt."
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: bool "Return value of datetime_has_tz."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Return True if datetime dt has tzinfo else False\n\n    Args:\n        dt: datetime.datetime\n\n    Returns:\n        True if dt is timezone aware, else False\n\n    Raises:\n        TypeError if dt is not a datetime.datetime object\n    '. RESULT expression_result]
            [COMMAND Return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None. RESULT result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

    [ALTERNATIVE_FLOW: When not isinstance(dt, datetime.datetime)]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

[END_WORKER]
```

</details>

<a id="fn-datetime_tzutils-py-datetime_naive_to_local"></a>
#### Function: datetime_naive_to_local

- key: `datetime_tzutils.py::datetime_naive_to_local`
- spl_line_count: 29

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Convert naive (timezone unaware) datetime.datetime" datetime_naive_to_local]
    [INPUTS]
        <REF> dt </REF>: datetime.datetime "Input parameter dt."
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: datetime.datetime "Return value of datetime_naive_to_local."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Convert naive (timezone unaware) datetime.datetime\n        to aware timezone in local timezone\n\n    Args:\n        dt: datetime.datetime without timezone\n\n    Returns:\n        datetime.datetime with local timezone\n\n    Raises:\n        TypeError if dt is not a datetime.datetime object\n        ValueError if dt is not a naive/timezone unaware object\n    '. RESULT expression_result]
            [COMMAND Return dt.replace(tzinfo=get_local_tz(dt)). This step relies on helper get_local_tz: Return local timezone as datetime.timezone tzinfo for naive datetime dt RESULT result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

    [ALTERNATIVE_FLOW: When not isinstance(dt, datetime.datetime)]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

    [ALTERNATIVE_FLOW: When dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

[END_WORKER]
```

</details>

<a id="fn-datetime_tzutils-py-datetime_naive_to_utc"></a>
#### Function: datetime_naive_to_utc

- key: `datetime_tzutils.py::datetime_naive_to_utc`
- spl_line_count: 29

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Convert naive (timezone unaware) datetime.datetime" datetime_naive_to_utc]
    [INPUTS]
        <REF> dt </REF>: datetime.datetime "Input parameter dt."
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: datetime.datetime "Return value of datetime_naive_to_utc."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Convert naive (timezone unaware) datetime.datetime\n        to aware timezone in UTC timezone\n\n    Args:\n        dt: datetime.datetime without timezone\n\n    Returns:\n        datetime.datetime with UTC timezone\n\n    Raises:\n        TypeError if dt is not a datetime.datetime object\n        ValueError if dt is not a naive/timezone unaware object\n    '. RESULT expression_result]
            [COMMAND Return dt.replace(tzinfo=datetime.timezone.utc). RESULT result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

    [ALTERNATIVE_FLOW: When not isinstance(dt, datetime.datetime)]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

    [ALTERNATIVE_FLOW: When dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

[END_WORKER]
```

</details>

<a id="fn-datetime_tzutils-py-datetime_remove_tz"></a>
#### Function: datetime_remove_tz

- key: `datetime_tzutils.py::datetime_remove_tz`
- spl_line_count: 23

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Remove timezone from a datetime.datetime object" datetime_remove_tz]
    [INPUTS]
        <REF> dt </REF>: datetime.datetime "Input parameter dt."
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: datetime.datetime "Return value of datetime_remove_tz."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Remove timezone from a datetime.datetime object\n\n    Args:\n        dt: datetime.datetime object with tzinfo\n\n    Returns:\n        dt without any timezone info (naive datetime object)\n\n    Raises:\n        TypeError if dt is not a datetime.datetime object\n    '. RESULT expression_result]
            [COMMAND Return dt.replace(tzinfo=None). RESULT result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

    [ALTERNATIVE_FLOW: When not isinstance(dt, datetime.datetime)]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

[END_WORKER]
```

</details>

<a id="fn-datetime_tzutils-py-datetime_to_new_tz"></a>
#### Function: datetime_to_new_tz

- key: `datetime_tzutils.py::datetime_to_new_tz`
- spl_line_count: 32

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Convert datetime.datetime object from current timezone to new timezone with offset of seconds from UTC" datetime_to_new_tz]
    [INPUTS]
        <REF> dt </REF>: datetime.datetime "Input parameter dt."
        <REF> offset </REF>: data_type "Input parameter offset."
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: datetime.datetime "Return value of datetime_to_new_tz."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Convert datetime.datetime object from current timezone to new timezone with offset of seconds from UTC\n\n    Args:\n        dt: datetime.datetime object\n\n    Returns:\n        datetime.datetime object in new timezone\n\n    Raises:\n        TypeError if dt is not a datetime.datetime object\n        ValueError if dt is not timezone aware\n    '. RESULT expression_result]
            [COMMAND Assign datetime.timedelta(seconds=offset) to time_delta. RESULT time_delta]
            [COMMAND Assign datetime.timezone(time_delta) to tz. RESULT tz]
            [COMMAND Return dt.astimezone(tz=tz). RESULT result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

    [ALTERNATIVE_FLOW: When not isinstance(dt, datetime.datetime)]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

    [ALTERNATIVE_FLOW: When not datetime_has_tz(dt)]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

[END_WORKER]
```

</details>

<a id="fn-datetime_tzutils-py-datetime_tz_to_utc"></a>
#### Function: datetime_tz_to_utc

- key: `datetime_tzutils.py::datetime_tz_to_utc`
- spl_line_count: 29

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Convert datetime.datetime object with timezone to UTC timezone" datetime_tz_to_utc]
    [INPUTS]
        <REF> dt </REF>: datetime.datetime "Input parameter dt."
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: datetime.datetime "Return value of datetime_tz_to_utc."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Convert datetime.datetime object with timezone to UTC timezone\n\n    Args:\n        dt: datetime.datetime object\n\n    Returns:\n        datetime.datetime in UTC timezone\n\n    Raises:\n        TypeError if dt is not datetime.datetime object\n        ValueError if dt does not have timezone information\n    '. RESULT expression_result]
            [COMMAND Evaluate condition dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None and continue with the fallback branch when needed. RESULT branch_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

    [ALTERNATIVE_FLOW: When not isinstance(dt, datetime.datetime)]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

    [ALTERNATIVE_FLOW: When dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None]
        [SEQUENTIAL_BLOCK]
            [COMMAND Return dt.astimezone(tz=datetime.timezone.utc). RESULT result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

[END_WORKER]
```

</details>

<a id="fn-datetime_tzutils-py-datetime_utc_to_local"></a>
#### Function: datetime_utc_to_local

- key: `datetime_tzutils.py::datetime_utc_to_local`
- spl_line_count: 29

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Convert datetime.datetime object in UTC timezone to local timezone" datetime_utc_to_local]
    [INPUTS]
        <REF> dt </REF>: datetime.datetime "Input parameter dt."
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: datetime.datetime "Return value of datetime_utc_to_local."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Convert datetime.datetime object in UTC timezone to local timezone\n\n    Args:\n        dt: datetime.datetime object\n\n    Returns:\n        datetime.datetime in local timezone\n\n    Raises:\n        TypeError if dt is not a datetime.datetime object\n        ValueError if dt is not in UTC timezone\n    '. RESULT expression_result]
            [COMMAND Return dt.astimezone(tz=None). RESULT result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

    [ALTERNATIVE_FLOW: When not isinstance(dt, datetime.datetime)]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

    [ALTERNATIVE_FLOW: When dt.tzinfo is not datetime.timezone.utc]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

[END_WORKER]
```

</details>

<a id="fn-datetime_tzutils-py-get_local_tz"></a>
#### Function: get_local_tz

- key: `datetime_tzutils.py::get_local_tz`
- spl_line_count: 29

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Return local timezone as datetime.timezone tzinfo for naive datetime dt" get_local_tz]
    [INPUTS]
        <REF> dt </REF>: datetime.datetime "Input parameter dt."
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: datetime.tzinfo "Return value of get_local_tz."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Return local timezone as datetime.timezone tzinfo for naive datetime dt\n\n    Args:\n        dt: datetime.datetime object\n\n    Returns:\n        local timezone for dt as datetime.timezone\n\n    Raises:\n        TypeError if dt is not datetime.datetime object\n    '. RESULT expression_result]
            [COMMAND Return dt.astimezone().tzinfo. RESULT result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

    [ALTERNATIVE_FLOW: When not isinstance(dt, datetime.datetime)]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

    [ALTERNATIVE_FLOW: When datetime_has_tz(dt)]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

[END_WORKER]
```

</details>

<a id="fn-datetime_tzutils-py-utc_offset_seconds"></a>
#### Function: utc_offset_seconds

- key: `datetime_tzutils.py::utc_offset_seconds`
- spl_line_count: 29

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Return offset in seconds from UTC for timezone aware datetime.datetime object" utc_offset_seconds]
    [INPUTS]
        <REF> dt </REF>: datetime.datetime "Input parameter dt."
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: int "Return value of utc_offset_seconds."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Return offset in seconds from UTC for timezone aware datetime.datetime object\n\n    Args:\n        dt: datetime.datetime object\n\n    Returns:\n        offset in seconds from UTC\n\n    Raises:\n        ValueError if dt does not have timezone information\n        TypeError if dt is not a datetime.datetime object\n    '. RESULT expression_result]
            [COMMAND Evaluate condition dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None and continue with the fallback branch when needed. RESULT branch_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

    [ALTERNATIVE_FLOW: When not isinstance(dt, datetime.datetime)]
        [SEQUENTIAL_BLOCK]
            [COMMAND Execute statement Raise. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

    [ALTERNATIVE_FLOW: When dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None]
        [SEQUENTIAL_BLOCK]
            [COMMAND Return dt.tzinfo.utcoffset(dt).total_seconds(). RESULT result]
        [END_SEQUENTIAL_BLOCK]
    [END_ALTERNATIVE_FLOW]

[END_WORKER]
```

</details>

<a id="module-test_datetime_tzutils-py"></a>
### Module: test_datetime_tzutils.py

- function_count: 19

<a id="fn-test_datetime_tzutils-py-test_datetime_has_tz"></a>
#### Function: test_datetime_has_tz

- key: `test_datetime_tzutils.py::test_datetime_has_tz`
- spl_line_count: 17

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "test_datetime_has_tz coordinates local logic and helper calls such as datetime_has_tz." test_datetime_has_tz]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_datetime_has_tz."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Assign datetime.timezone(offset=datetime.timedelta(seconds=-28800)) to tz. RESULT tz]
            [COMMAND Assign datetime.datetime(2020, 9, 1, 21, 10, 0, tzinfo=tz) to dt. RESULT dt]
            [COMMAND Execute statement Assert. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_datetime_naive_to_local"></a>
#### Function: test_datetime_naive_to_local

- key: `test_datetime_tzutils.py::test_datetime_naive_to_local`
- spl_line_count: 19

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "test_datetime_naive_to_local coordinates local logic and helper calls such as datetime_naive_to_local." test_datetime_naive_to_local]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_datetime_naive_to_local."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Assign datetime.datetime(2020, 9, 1, 12, 0, 0) to dt. RESULT dt]
            [COMMAND Assign tzlocal.get_localzone().utcoffset(dt) to tz_offset. RESULT tz_offset]
            [COMMAND Assign datetime.timezone(offset=tz_offset) to tz. RESULT tz]
            [COMMAND Assign datetime_tzutils.datetime_naive_to_local(dt) to local. This step relies on helper datetime_naive_to_local: Convert naive (timezone unaware) datetime.datetime RESULT local]
            [COMMAND Execute statement Assert. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_datetime_naive_to_utc"></a>
#### Function: test_datetime_naive_to_utc

- key: `test_datetime_tzutils.py::test_datetime_naive_to_utc`
- spl_line_count: 17

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "test_datetime_naive_to_utc coordinates local logic and helper calls such as datetime_naive_to_utc." test_datetime_naive_to_utc]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_datetime_naive_to_utc."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Assign datetime.datetime(2020, 9, 1, 12, 0, 0) to dt. RESULT dt]
            [COMMAND Assign datetime_tzutils.datetime_naive_to_utc(dt) to utc. This step relies on helper datetime_naive_to_utc: Convert naive (timezone unaware) datetime.datetime RESULT utc]
            [COMMAND Execute statement Assert. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_datetime_remove_tz"></a>
#### Function: test_datetime_remove_tz

- key: `test_datetime_tzutils.py::test_datetime_remove_tz`
- spl_line_count: 19

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "test_datetime_remove_tz coordinates local logic and helper calls such as datetime_remove_tz, datetime_has_tz." test_datetime_remove_tz]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_datetime_remove_tz."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Assign datetime.timezone(offset=datetime.timedelta(seconds=-25200)) to tz. RESULT tz]
            [COMMAND Assign datetime.datetime(2020, 9, 1, 22, 6, 0, tzinfo=tz) to dt. RESULT dt]
            [COMMAND Assign datetime_tzutils.datetime_remove_tz(dt) to dt. This step relies on helper datetime_remove_tz: Remove timezone from a datetime.datetime object RESULT dt]
            [COMMAND Execute statement Assert. RESULT statement_result]
            [COMMAND Execute statement Assert. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_datetime_to_new_tz"></a>
#### Function: test_datetime_to_new_tz

- key: `test_datetime_tzutils.py::test_datetime_to_new_tz`
- spl_line_count: 22

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Test datetime_to_new_tz" test_datetime_to_new_tz]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_datetime_to_new_tz."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Test datetime_to_new_tz'. RESULT expression_result]
            [COMMAND Assign datetime.timezone(offset=datetime.timedelta(seconds=-25200)) to tz. RESULT tz]
            [COMMAND Assign datetime.datetime(2021, 10, 1, 0, 30, 0, tzinfo=tz) to dt. RESULT dt]
            [COMMAND Assign datetime_tzutils.datetime_to_new_tz(dt, 0) to dt_new. This step relies on helper datetime_to_new_tz: Convert datetime.datetime object from current timezone to new timezone with offset of seconds from UTC RESULT dt_new]
            [COMMAND Execute statement Assert. RESULT statement_result]
            [COMMAND Assign datetime_tzutils.datetime_to_new_tz(dt, 3600) to dt_new. This step relies on helper datetime_to_new_tz: Convert datetime.datetime object from current timezone to new timezone with offset of seconds from UTC RESULT dt_new]
            [COMMAND Assign datetime.timezone(offset=datetime.timedelta(seconds=3600)) to tz_new. RESULT tz_new]
            [COMMAND Execute statement Assert. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_datetime_to_new_tz_type_error"></a>
#### Function: test_datetime_to_new_tz_type_error

- key: `test_datetime_tzutils.py::test_datetime_to_new_tz_type_error`
- spl_line_count: 16

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Test datetime_to_new_tz with invalid dt" test_datetime_to_new_tz_type_error]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_datetime_to_new_tz_type_error."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Test datetime_to_new_tz with invalid dt'. RESULT expression_result]
            [COMMAND Execute statement With. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_datetime_to_new_tz_value_error"></a>
#### Function: test_datetime_to_new_tz_value_error

- key: `test_datetime_tzutils.py::test_datetime_to_new_tz_value_error`
- spl_line_count: 17

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Test datetime_to_new_tz with invalid dt" test_datetime_to_new_tz_value_error]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_datetime_to_new_tz_value_error."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Test datetime_to_new_tz with invalid dt'. RESULT expression_result]
            [COMMAND Assign datetime.datetime(2021, 10, 1, 0, 30, 0) to dt. RESULT dt]
            [COMMAND Execute statement With. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_datetime_tz_to_utc"></a>
#### Function: test_datetime_tz_to_utc

- key: `test_datetime_tzutils.py::test_datetime_tz_to_utc`
- spl_line_count: 18

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "test_datetime_tz_to_utc coordinates local logic and helper calls such as datetime_tz_to_utc." test_datetime_tz_to_utc]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_datetime_tz_to_utc."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Assign pytz.timezone('US/Pacific') to tz. RESULT tz]
            [COMMAND Assign tz.localize(datetime.datetime(2020, 12, 1, 22, 6, 0)) to dt. RESULT dt]
            [COMMAND Assign datetime_tzutils.datetime_tz_to_utc(dt) to utc. This step relies on helper datetime_tz_to_utc: Convert datetime.datetime object with timezone to UTC timezone RESULT utc]
            [COMMAND Execute statement Assert. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_datetime_tz_to_utc_dst"></a>
#### Function: test_datetime_tz_to_utc_dst

- key: `test_datetime_tzutils.py::test_datetime_tz_to_utc_dst`
- spl_line_count: 18

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "test_datetime_tz_to_utc_dst coordinates local logic and helper calls such as datetime_tz_to_utc." test_datetime_tz_to_utc_dst]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_datetime_tz_to_utc_dst."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Assign pytz.timezone('US/Pacific') to tz. RESULT tz]
            [COMMAND Assign tz.localize(datetime.datetime(2020, 5, 1, 22, 6, 0)) to dt. RESULT dt]
            [COMMAND Assign datetime_tzutils.datetime_tz_to_utc(dt) to utc. This step relies on helper datetime_tz_to_utc: Convert datetime.datetime object with timezone to UTC timezone RESULT utc]
            [COMMAND Execute statement Assert. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_datetime_utc_to_local"></a>
#### Function: test_datetime_utc_to_local

- key: `test_datetime_tzutils.py::test_datetime_utc_to_local`
- spl_line_count: 18

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "test_datetime_utc_to_local coordinates local logic and helper calls such as datetime_utc_to_local." test_datetime_utc_to_local]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_datetime_utc_to_local."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Assign datetime.datetime(2020, 9, 1, 19, 0, 0, tzinfo=datetime.timezone.utc) to utc. RESULT utc]
            [COMMAND Assign datetime_tzutils.datetime_utc_to_local(utc) to dt. This step relies on helper datetime_utc_to_local: Convert datetime.datetime object in UTC timezone to local timezone RESULT dt]
            [COMMAND Assign tzlocal.get_localzone() to tz. RESULT tz]
            [COMMAND Execute statement Assert. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_datetime_utc_to_local_error_not_utc"></a>
#### Function: test_datetime_utc_to_local_error_not_utc

- key: `test_datetime_tzutils.py::test_datetime_utc_to_local_error_not_utc`
- spl_line_count: 17

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Assert ValueError is raised if dt is not UTC timezone" test_datetime_utc_to_local_error_not_utc]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_datetime_utc_to_local_error_not_utc."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Assert ValueError is raised if dt is not UTC timezone'. RESULT expression_result]
            [COMMAND Assign datetime.datetime(2020, 9, 1, 19, 0, 0, tzinfo=datetime.timezone(offset=datetime.timedelta(seconds=-25200))) to utc. RESULT utc]
            [COMMAND Execute statement With. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_get_local_tz"></a>
#### Function: test_get_local_tz

- key: `test_datetime_tzutils.py::test_get_local_tz`
- spl_line_count: 18

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "test_get_local_tz coordinates local logic and helper calls such as get_local_tz." test_get_local_tz]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_get_local_tz."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Assign datetime.datetime(2020, 12, 1, 21, 10, 0) to dt. RESULT dt]
            [COMMAND Assign datetime_tzutils.get_local_tz(dt) to tz. This step relies on helper get_local_tz: Return local timezone as datetime.timezone tzinfo for naive datetime dt RESULT tz]
            [COMMAND Assign tzlocal.get_localzone().utcoffset(dt) to tz_offset. RESULT tz_offset]
            [COMMAND Execute statement Assert. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_get_local_tz_dst"></a>
#### Function: test_get_local_tz_dst

- key: `test_datetime_tzutils.py::test_get_local_tz_dst`
- spl_line_count: 18

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "test_get_local_tz_dst coordinates local logic and helper calls such as get_local_tz." test_get_local_tz_dst]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_get_local_tz_dst."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Assign datetime.datetime(2020, 9, 1, 21, 10, 0) to dt. RESULT dt]
            [COMMAND Assign datetime_tzutils.get_local_tz(dt) to tz. This step relies on helper get_local_tz: Return local timezone as datetime.timezone tzinfo for naive datetime dt RESULT tz]
            [COMMAND Assign tzlocal.get_localzone().utcoffset(dt) to tz_offset. RESULT tz_offset]
            [COMMAND Execute statement Assert. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_get_local_tz_error"></a>
#### Function: test_get_local_tz_error

- key: `test_datetime_tzutils.py::test_get_local_tz_error`
- spl_line_count: 18

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Test get_local_tz raises ValueError if dt is timezone aware" test_get_local_tz_error]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_get_local_tz_error."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Test get_local_tz raises ValueError if dt is timezone aware'. RESULT expression_result]
            [COMMAND Assign datetime.timezone(offset=datetime.timedelta(seconds=-28800)) to tz. RESULT tz]
            [COMMAND Assign datetime.datetime(2020, 9, 1, 21, 10, 0, tzinfo=tz) to dt. RESULT dt]
            [COMMAND Execute statement With. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_not_datetime_has_tz"></a>
#### Function: test_not_datetime_has_tz

- key: `test_datetime_tzutils.py::test_not_datetime_has_tz`
- spl_line_count: 16

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "test_not_datetime_has_tz coordinates local logic and helper calls such as datetime_has_tz." test_not_datetime_has_tz]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_not_datetime_has_tz."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Assign datetime.datetime(2020, 9, 1, 21, 10, 0) to dt. RESULT dt]
            [COMMAND Execute statement Assert. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_type_error"></a>
#### Function: test_type_error

- key: `test_datetime_tzutils.py::test_type_error`
- spl_line_count: 17

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Test TypeError is raised if method is not a datetime method" test_type_error]
    [INPUTS]
        <REF> method </REF>: data_type "Input parameter method."
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_type_error."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Test TypeError is raised if method is not a datetime method'. RESULT expression_result]
            [COMMAND Execute statement With. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_utc_offset_seconds"></a>
#### Function: test_utc_offset_seconds

- key: `test_datetime_tzutils.py::test_utc_offset_seconds`
- spl_line_count: 18

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "test_utc_offset_seconds coordinates local logic and helper calls such as utc_offset_seconds." test_utc_offset_seconds]
    [INPUTS]
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_utc_offset_seconds."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Assign datetime.datetime(2021, 9, 1, 0, 0, 0, 0, tzinfo=datetime.timezone.utc) to dt_utc. RESULT dt_utc]
            [COMMAND Execute statement Assert. RESULT statement_result]
            [COMMAND Assign datetime.datetime(2021, 9, 1, 0, 0, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=-7))) to dt_pdt. RESULT dt_pdt]
            [COMMAND Execute statement Assert. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_value_error_naive"></a>
#### Function: test_value_error_naive

- key: `test_datetime_tzutils.py::test_value_error_naive`
- spl_line_count: 17

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Test ValueError raised if naive datetime passed to method" test_value_error_naive]
    [INPUTS]
        <REF> method </REF>: data_type "Input parameter method."
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_value_error_naive."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Test ValueError raised if naive datetime passed to method'. RESULT expression_result]
            [COMMAND Execute statement With. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>

<a id="fn-test_datetime_tzutils-py-test_value_error_not_naive"></a>
#### Function: test_value_error_not_naive

- key: `test_datetime_tzutils.py::test_value_error_not_naive`
- spl_line_count: 17

<details>
<summary>View SPL</summary>

```spl
[DEFINE_WORKER: "Test ValueError raised if timezone aware datetime passed to method" test_value_error_not_naive]
    [INPUTS]
        <REF> method </REF>: data_type "Input parameter method."
    [END_INPUTS]

    [OUTPUTS]
        <REF> result </REF>: data_type "Return value of test_value_error_not_naive."
    [END_OUTPUTS]

    [MAIN_FLOW]
        [SEQUENTIAL_BLOCK]
            [COMMAND Evaluate 'Test ValueError raised if timezone aware datetime passed to method'. RESULT expression_result]
            [COMMAND Execute statement With. RESULT statement_result]
        [END_SEQUENTIAL_BLOCK]
    [END_MAIN_FLOW]

[END_WORKER]
```

</details>
