# cqueue


[![PyPI version](https://badge.fury.io/py/cqueue.svg)](https://badge.fury.io/py/cqueue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This library was created to make the concept of a queue easier by visualizing it and showing how items enter and exit it, especially for beginners in data structures


## Installation


You can install `cqueue` via pip:


```bash
pip install cqueue
```


## Usage 


### For Circular Queue


```python
from cqueue import circularQueue

x = circularQueue(capacity=7)
print(x)
```


### Output


```bash
[]
```


#### You Can Visualize The Queue With All Details


```python
from cqueue import circularQueue

x = circularQueue(capacity=7, detail=True)
print(x)
```


### Output


```bash
╒═════════╤══╤══╤══╤══╤══╤══╤══╤══════════╕
│ <- EXIT │  │  │  │  │  │  │  │ <- ENTER │
╘═════════╧══╧══╧══╧══╧══╧══╧══╧══════════╛
```


#### Enqueue


```python
from cqueue import circularQueue

x = circularQueue(capacity=7, detail=True)
print(x)
x.enqueue(1)
x.enqueue(2)
x.enqueue(3)
print(x)
```


### Output


```bash
╒═════════╤══╤══╤══╤══╤══╤══╤══╤══════════╕
│ <- EXIT │  │  │  │  │  │  │  │ <- ENTER │
╘═════════╧══╧══╧══╧══╧══╧══╧══╧══════════╛
╒═════════╤═══╤═══╤═══╤══╤══╤══╤══╤══════════╕
│ <- EXIT │ 1 │ 2 │ 3 │  │  │  │  │ <- ENTER │
╘═════════╧═══╧═══╧═══╧══╧══╧══╧══╧══════════╛
```


#### Dequeue


```python
from cqueue import circularQueue

x = circularQueue([1, 2, 3], capacity=7, detail=True)
print(x)
x.dequeue()
print(x)
```


### Output


```bash
╒═════════╤═══╤═══╤═══╤══╤══╤══╤══╤══════════╕
│ <- EXIT │ 1 │ 2 │ 3 │  │  │  │  │ <- ENTER │
╘═════════╧═══╧═══╧═══╧══╧══╧══╧══╧══════════╛
╒═════════╤═══╤═══╤══╤══╤══╤══╤══╤══════════╕
│ <- EXIT │ 2 │ 3 │  │  │  │  │  │ <- ENTER │
╘═════════╧═══╧═══╧══╧══╧══╧══╧══╧══════════╛
```


#### You Can Check If The Queue Is Empty Or Not


```python
from cqueue import circularQueue

x = circularQueue(capacity=7, detail=True)
print(x.isEmpty())
```


### Output


```bash
True
```

#### You Can Check If The Queue Is Full Or Not


```python
from cqueue import circularQueue

x = circularQueue([1, 2, 3, 4, 5, 6, 7], capacity=7, detail=True)
print(x.isFull())
```


### Output


```bash
True
```


#### You Can See The Item Who Can EXIT From The Queue Using peek Or top


```python
from cqueue import circularQueue

x = circularQueue([5, 6, 7], capacity=7, detail=True)
print(x.peek())
print(x.top())
```


### Output


```bash
5
5
```


#### You Can See How Many Items Are In The Queue Using len Function


```python
from cqueue import circularQueue

x = circularQueue([5, 6, 7], capacity=7, detail=True)
print(len(x))
```


### Output


```bash
3
```


#### You Can Clear The Queue


```python
from cqueue import circularQueue

x = circularQueue([5, 6, 7], capacity=7, detail=True)
print(x)
x.clear()
print(x)
```


### Output


```bash
╒═════════╤═══╤═══╤═══╤══╤══╤══╤══╤══════════╕
│ <- EXIT │ 5 │ 6 │ 7 │  │  │  │  │ <- ENTER │
╘═════════╧═══╧═══╧═══╧══╧══╧══╧══╧══════════╛
╒═════════╤══╤══╤══╤══╤══╤══╤══╤══════════╕
│ <- EXIT │  │  │  │  │  │  │  │ <- ENTER │
╘═════════╧══╧══╧══╧══╧══╧══╧══╧══════════╛
```


### For Linked Circular Queue


You can use linkedCircularQueue with the same syntax as circularQueue with all previous methods the main difference is circularQueue use static array(list) and linkedCircularQueue use static circular singly linked list


## License


This project is licensed under the MIT LICENSE - see the [LICENSE](https://opensource.org/licenses/MIT) for more details.
