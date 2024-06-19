# Mathematics Utilities

### Mathematics utilities in Python.

![PyPI](https://img.shields.io/pypi/v/nrt-math-utils?color=blueviolet&style=plastic)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nrt-math-utils?color=greens&style=plastic)
![PyPI - License](https://img.shields.io/pypi/l/nrt-math-utils?color=blue&style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dd/nrt-math-utils?style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nrt-math-utils?color=yellow&style=plastic)
[![Coverage Status](https://coveralls.io/repos/github/etuzon/python-nrt-math-utils/badge.svg)](https://coveralls.io/github/etuzon/pytohn-nrt-math-utils)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/etuzon/python-nrt-math-utils?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/etuzon/python-nrt-math-utils?style=plastic)
[![DeepSource](https://app.deepsource.com/gh/etuzon/python-nrt-math-utils.svg/?label=active+issues&show_trend=false&token=Ly6vE3lLp94vOwUzDfMzb9Oy)](https://app.deepsource.com/gh/etuzon/python-nrt-math-utils/)

## MathUtil class

### Methods

| **Method**       | **Description**                                                                                           | **Parameters**                                                                                             | **Returns**                                               |
|------------------|-----------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| `average`        | Calculates the weighted average of a list of numbers.                                                     | `numbers (list)` The list of numbers to calculate the average of.<br>`weights (list)` The list of weights. | `DecimalNumber` The average of the numbers.               |
| `floor`          | Returns the floor of a number.                                                                            | `number` The number to calculate the floor of.<br>`digits` Digits amount to cut from the number.           | `number type` The floor of the number.                    |
| `is_all_numbers` | Checks if all elements in a list are numbers.                                                             | `elements (list)` The list of elements to check.                                                           | `bool` True if all elements are numbers, False otherwise. |
| `max`            | Returns the maximum number from variable elements, which can be numbers or an iterable objects like list. | `*elements` Variable arguments, which can be numbers or an iterable objects like list.                     | `number type` The maximum number in the list.             |
| `min`            | Returns the minimum number from variable elements, which can be numbers or an iterable objects like list. | `*elements` Variable arguments, which can be numbers or an iterable objects like list.                     | `number type` The minimum number in the list.             |


### Examples:

- #### MathUtil.average

    **Code**
    ```python
    from math_utils import MathUtil
  
    # Calculate the weighted average of a list of numbers
    average = MathUtil.average([1, 2, 3, 4, 5], [1, 5, 6, 7, 8])
  
    print(average)
    ```
    **Output**
    ```
    3.592593
    ```
  
  - #### MathUtil.floor
        
    **Code**
    ```python
    from math_utils import MathUtil
  
    # Calculate the floor of a number
    floor = MathUtil.floor(3.14159, 2)
  
    print(floor)
    ```
    **Output**
    ```
    3.14
    ```

- #### MathUtil.is_all_numbers
  
    **Code**
    ```python
    from math_utils import MathUtil

    # Check if all elements in a list are numbers
    is_all_numbers = MathUtil.is_all_numbers([1, 2, 3, 4, 5])

    print(is_all_numbers)
    ```
    **Output**
    ```
    True
    ```

- #### MathUtil.max

    **Code**
    ```python
    from math_utils import MathUtil

    # Get the maximum number from a list
    max_number = MathUtil.max(1, [2, 7, [8, 9]], 3, 4, 5)

    print(max_number)
    ```
    **Output**
    ```
    9
    ```
  
- #### MathUtil.min
    
    **Code**
    ```python
    from math_utils import MathUtil

    # Get the minimum number from a list
    min_number = MathUtil.min(1, [2, 7, [0, 9]], 3, 4, 5)

    print(min_number)
    ```
    **Output**
    ```
    0
    ```

## DecimalNumber class

Represents a decimal number with a fixed number of decimal places.

### Examples:

- #### Create a DecimalNumber object

    **Code**
    ```python
    from math_utils import DecimalNumber

    # Create a DecimalNumber object with a value of 3.14159 and 2 decimal places
    decimal_number = DecimalNumber(3.14159, 2)

    print(decimal_number)
    ```
    **Output**
    ```
    3.14
    ```
  
- #### Create a DecimalNumber object with default decimal places

    **Code**
    ```python
    from math_utils import DecimalNumber

    # Create a DecimalNumber object with a value of 3.14159 and default 6 decimal places
    decimal_number = DecimalNumber(3.1415926535897)
    print(decimal_number)
    ```
  
    **Output**
    ```
    3.141593
    ```

- #### Add two DecimalNumber objects

    **Code**
    ```python
    from math_utils import DecimalNumber

    # Create two DecimalNumber objects
    decimal_number_1 = DecimalNumber(3.14159, 2)
    decimal_number_2 = DecimalNumber(2.71828, 2)

    # Add the two DecimalNumber objects
    result = decimal_number_1 + decimal_number_2

    print(result)
    ```
    **Output**
    ```
    5.86
    ```
  
- #### Subtract a number from DecimalNumber

    **Code**
    ```python
    from math_utils import DecimalNumber
  
    # Create a DecimalNumber object
    decimal_number = DecimalNumber(3.14159, 2)
    
    # Subtract a number from the DecimalNumber object
    result = decimal_number - 1.23456
    
    print(result)
    ```
  
    **Output**
    ```
    1.91
    ```

- #### Multiply DecimalNumber with other number

    **Code**
    ```python
    from math_utils import DecimalNumber
  
    # Create a DecimalNumber object
    decimal_number = DecimalNumber(3.14159, 2)
  
    # Multiply the DecimalNumber object with another number
    result = decimal_number * 2
    
    print(result)
    ```
  
    **Output**
    ```
    6.28
    ```
  
- #### Compare DecimalNumber to other number

    **Code**
    ```python
    from math_utils import DecimalNumber
  
    # Create a DecimalNumber object
    decimal_number = DecimalNumber(3.14159, 2)
    
    # Compare the DecimalNumber object to another number
    result = decimal_number > 3.14
    
    print(result)
    ```
  
    **Output**
    ```
    True
    ```
