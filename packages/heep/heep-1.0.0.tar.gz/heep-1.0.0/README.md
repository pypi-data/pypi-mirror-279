# heep


[![PyPI version](https://badge.fury.io/py/heep.svg)](https://badge.fury.io/py/heep)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This library was created to simplify the concept of a heap by showing that it is simply an array that is treated as a complete binary tree with some additional properties such as maximum and minimum binary heap that help us solve some programming issues such as array sorting and priority queue this library is specially designed for beginners in data structures 


## Installation


You can install `heep` via pip:


```bash
pip install heep
```


## Usage 


### For Min Binary Heap


```python
from heep import minBinaryHeap


x = minBinaryHeap([5, 4, 6, 2, 8, 1, 3, 7, 9])
print(x)
```


### Output


```bash
[1, 2, 3, 4, 8, 6, 5, 7, 9]
```


#### You Can Visualize The Heap With All Details (As A Complete Binary Tree)


```python
from heep import minBinaryHeap


x = minBinaryHeap([5, 4, 6, 2, 8, 1, 3, 7, 9], detail=True)
print(x)
```


### Output


```bash
╒════════════════╤══════════════╤═══════════════╕
│   Current node │ Left child   │ Right child   │
╞════════════════╪══════════════╪═══════════════╡
│              1 │ 2            │ 3             │
├────────────────┼──────────────┼───────────────┤
│              2 │ 4            │ 8             │
├────────────────┼──────────────┼───────────────┤
│              3 │ 6            │ 5             │
├────────────────┼──────────────┼───────────────┤
│              4 │ 7            │ 9             │
├────────────────┼──────────────┼───────────────┤
│              8 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              6 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              5 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              7 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              9 │ None         │ None          │
╘════════════════╧══════════════╧═══════════════╛
```


#### You Can Add A New Value To The Heap


```python
from heep import minBinaryHeap


x = minBinaryHeap([5, 4, 6, 2, 8, 1, 3, 7, 9], detail=True)
print(x)
x.add(0)
print(x)
```


### Output


```bash
╒════════════════╤══════════════╤═══════════════╕
│   Current node │ Left child   │ Right child   │
╞════════════════╪══════════════╪═══════════════╡
│              1 │ 2            │ 3             │
├────────────────┼──────────────┼───────────────┤
│              2 │ 4            │ 8             │
├────────────────┼──────────────┼───────────────┤
│              3 │ 6            │ 5             │
├────────────────┼──────────────┼───────────────┤
│              4 │ 7            │ 9             │
├────────────────┼──────────────┼───────────────┤
│              8 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              6 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              5 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              7 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              9 │ None         │ None          │
╘════════════════╧══════════════╧═══════════════╛
╒════════════════╤══════════════╤═══════════════╕
│   Current node │ Left child   │ Right child   │
╞════════════════╪══════════════╪═══════════════╡
│              0 │ 1            │ 3             │
├────────────────┼──────────────┼───────────────┤
│              1 │ 4            │ 2             │
├────────────────┼──────────────┼───────────────┤
│              3 │ 6            │ 5             │
├────────────────┼──────────────┼───────────────┤
│              4 │ 7            │ 9             │
├────────────────┼──────────────┼───────────────┤
│              2 │ 8            │ None          │
├────────────────┼──────────────┼───────────────┤
│              6 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              5 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              7 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              9 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              8 │ None         │ None          │
╘════════════════╧══════════════╧═══════════════╛
```


#### You Can Get The Min Value In The Heap


```python
from heep import minBinaryHeap


x = minBinaryHeap([5, 4, 6, 2, 8, 1, 3, 7, 9], detail=True)
print(x.get_min())
```


### Output


```bash
1
```


#### You Can Extract The Min Value In The Heap (Get The Min Value And Delete It)


```python
from heep import minBinaryHeap


x = minBinaryHeap([5, 4, 6, 2, 8, 1, 3, 7, 9], detail=True)
print(x)
print(f"Extracted Value: {x.extract_min()}")
print(x)
```


### Output


```bash
╒════════════════╤══════════════╤═══════════════╕
│   Current node │ Left child   │ Right child   │
╞════════════════╪══════════════╪═══════════════╡
│              1 │ 2            │ 3             │
├────────────────┼──────────────┼───────────────┤
│              2 │ 4            │ 8             │
├────────────────┼──────────────┼───────────────┤
│              3 │ 6            │ 5             │
├────────────────┼──────────────┼───────────────┤
│              4 │ 7            │ 9             │
├────────────────┼──────────────┼───────────────┤
│              8 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              6 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              5 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              7 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              9 │ None         │ None          │
╘════════════════╧══════════════╧═══════════════╛
Extracted Value: 1
╒════════════════╤══════════════╤═══════════════╕
│   Current node │ Left child   │ Right child   │
╞════════════════╪══════════════╪═══════════════╡
│              2 │ 4            │ 3             │
├────────────────┼──────────────┼───────────────┤
│              4 │ 7            │ 8             │
├────────────────┼──────────────┼───────────────┤
│              3 │ 6            │ 5             │
├────────────────┼──────────────┼───────────────┤
│              7 │ 9            │ None          │
├────────────────┼──────────────┼───────────────┤
│              8 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              6 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              5 │ None         │ None          │
├────────────────┼──────────────┼───────────────┤
│              9 │ None         │ None          │
╘════════════════╧══════════════╧═══════════════╛
```

#### You Can Know How Many Values In The Heap


```python
from heep import minBinaryHeap


x = minBinaryHeap([5, 4, 6, 2, 8, 1, 3, 7, 9], detail=True)
print(len(x))
```


### Output


```bash
9
```


### Note


The same methods in maxBinaryHeap with get_max and extract_max.


## License


This project is licensed under the MIT LICENSE - see the [LICENSE](https://opensource.org/licenses/MIT) for more details.
