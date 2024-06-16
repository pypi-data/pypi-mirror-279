![Random Choice](./images/randomChoice.jpg)


# randomChoice.py

`randomChoice.py` is a Python module that provides functions for selecting random elements from various data structures such as lists, tuples, sets, and dictionaries.




## Installation

Simply download `randomChoice.py` and place it in your project directory. It does not require any external dependencies beyond Python's standard library.

```bash
  from randomChoice import random_value
```
    

## Usage/Examples

```Python
from randomChoice import random_value

# Example usage
array = ["rays", "sun", "moon", "earth"]
tuple_obj = ("apple", "banana", "cherry")
set_obj = {"apple", "banana", "cherry"}
dict_obj = {1: "house", 5: "road", 8: "shop", 3: "store"}

print(random_element(array))      # Random element from array
print(random_element(tuple_obj))  # Random element from tuple
print(random_element(set_obj))    # Random element from set
print(random_element(dict_obj))   # Random value from dict

```

###  Function random_value

#### Parameters
* `obj` (list or tuple or set or dict): The input list, tuple, set, or dictionary from which to select a random element.
#### Returns
* Returns a random element from the input list, tuple, or set.
* Returns a random key-value pair (tuple) from the input dictionary.
#### Raises
* `TypeError`: If the input is not a list, tuple, set, or dictionary.


## License

[MIT](https://choosealicense.com/licenses/mit/)


## 🚀 About Me
I'm a student full stack developer at Atlas School, Tulsa...


## Authors

* [Frandy Slueue](https://www.github.com/frandy4ever)
* Email: [Frandy4ever@gmail.com](https://frandy4ever@gmail.com)
