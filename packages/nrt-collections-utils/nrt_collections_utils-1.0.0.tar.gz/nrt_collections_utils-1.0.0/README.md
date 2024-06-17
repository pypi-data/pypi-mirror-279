# Collections Utilities

### Collections utilities in Python.

![PyPI](https://img.shields.io/pypi/v/nrt-collections-utils?color=blueviolet&style=plastic)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nrt-collections-utils?color=greens&style=plastic)
![PyPI - License](https://img.shields.io/pypi/l/nrt-collections-utils?color=blue&style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dd/nrt-collections-utils?style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nrt-collections-utils?color=yellow&style=plastic)
[![Coverage Status](https://coveralls.io/repos/github/etuzon/python-nrt-collections-utils/badge.svg)](https://coveralls.io/github/etuzon/pytohn-nrt-collections-utils)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/etuzon/python-nrt-collections-utils?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/etuzon/python-nrt-collections-utils?style=plastic)
[![DeepSource](https://app.deepsource.com/gh/etuzon/python-nrt-collections-utils.svg/?label=active+issues&show_trend=false&token=6DkafEgUmnMb_ExVLT-07eDM)](https://app.deepsource.com/gh/etuzon/python-nrt-collections-utils/)

## CollectionsUtil class

### Methods

| **Method**          | **Description**                        | **Parameters**                        | **Returns**                               |
|---------------------|----------------------------------------|---------------------------------------|-------------------------------------------|
| `deep_args_to_list` | Flat deep structure arguments to list. | `args (tuple)` The arguments to flat. | `list` A flatten list.                    |
| `is_iter`           | Check if object is iterable.           | `obj` The object to check.            | `bool` True if iterable, False otherwise. |

### Examples:

- #### CollectionsUtil.deep_args_to_list

    **Code**
    ```python
    from collections_utils import CollectionsUtil

    # Flat deep structure arguments to list
    flat_args = CollectionsUtil.deep_args_to_list(1, 2, (3, 4, (5, 6, (7, 8, 9))))
    print(flat_args)
    ```
    **Output**
    ```
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ```
- #### CollectionsUtil.is_iter

  **Code**
    ```python
    from collections_utils import CollectionsUtil

    # Check if object is iterable
    print(CollectionsUtil.is_iter(1))
    print(CollectionsUtil.is_iter([1, 2, 3]))
    ```
    **Output**
    ```
    False
    True
    ```

## ListUtil class

### Methods

| **Method**          | **Description**     | **Parameters**                                      | **Returns**                                      |
|---------------------|---------------------|-----------------------------------------------------|--------------------------------------------------|
| `compare_lists`     | Compare two lists.  | `list_1 (list)` List 1.<br>`list_2 (list)` List 2.  | `bool` True if lists are equal, False otherwise. |
| `remove_none`       | Remove None values. | `list_ (list)` The list to remove None values from. | `list` The list without None values.             |
| `remove_duplicates` | Remove duplicates.  | `list_ (list)` The list to remove duplicates from.  | `list` The list without duplicates.              |

### Examples:

- #### ListUtil.compare_lists

    **Code**
    ```python
    from collections_utils import ListUtil

    # Compare two lists
    print(ListUtil.compare_lists([1, 3, 2], [1, 2, 3]))
    print(ListUtil.compare_lists([1, 2, 3], [1, 2, 4]))
    ```
    **Output**
    ```
    True
    False
    ```
  
- #### ListUtil.remove_none

    **Code**
    ```python
    from collections_utils import ListUtil

    # Remove None values
    print(ListUtil.remove_none([1, None, 2, None, 3]))
    ```
    **Output**
    ```
    [1, 2, 3]
    ```
  
- #### ListUtil.remove_duplicates

    **Code**
    ```python
    from collections_utils import ListUtil

    # Remove duplicates
    print(ListUtil.remove_duplicates([1, 2, 3, 1, 2, 3]))
    ```
    **Output**
    ```
    [1, 2, 3]
    ```
