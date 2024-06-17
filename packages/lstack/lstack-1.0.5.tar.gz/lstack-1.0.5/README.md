# lstack


[![PyPI version](https://badge.fury.io/py/lstack.svg)](https://badge.fury.io/py/lstack)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This library was created to make the stack concept easier to understand by visualizing it and showing how objects enter and exit the stack, especially for beginners in data structures 


## Installation


You can install `lstack` via pip:


```bash
pip install lstack
```


## Usage 


```python
from lstack import linkedStack

x = linkedStack(capacity=7)
print(x)
```


### Output


```bash
[]
```


#### You Can Visualize The Stack With All Details


```python
from lstack import linkedStack

x = linkedStack(capacity=7, detail=True)
print(x)
```


### Output


```bash
╒════════════╕
│ ENTER  ^   │
│   |    |   │
│   v   EXIT │
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
╘════════════╛
```


#### Push


```python
from lstack import linkedStack

x = linkedStack(capacity=7, detail=True)
print(x)
x.push(1)
x.push(2)
x.push(3)
print(x)
```


### Output


```bash
╒════════════╕
│ ENTER  ^   │
│   |    |   │
│   v   EXIT │
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
╘════════════╛
╒════════════╕
│ ENTER  ^   │
│   |    |   │
│   v   EXIT │
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
│ 3          │
├────────────┤
│ 2          │
├────────────┤
│ 1          │
╘════════════╛
```


#### Pop


```python
from lstack import linkedStack

x = linkedStack([1, 2, 3], capacity=7, detail=True)
print(x)
x.pop()
print(x)
```


### Output


```bash
╒════════════╕
│ ENTER  ^   │
│   |    |   │
│   v   EXIT │
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
│ 3          │
├────────────┤
│ 2          │
├────────────┤
│ 1          │
╘════════════╛
╒════════════╕
│ ENTER  ^   │
│   |    |   │
│   v   EXIT │
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
│ 2          │
├────────────┤
│ 1          │
╘════════════╛
```


#### You Can Check If The Stack Is Empty Or Not


```python
from lstack import linkedStack

x = linkedStack(capacity=7, detail=True)
print(x.isEmpty())
```


### Output


```bash
True
```

#### You Can Check If The Stack Is Full Or Not


```python
from lstack import linkedStack

x = linkedStack([1, 2, 3, 4, 5, 6, 7], capacity=7, detail=True)
print(x.isFull())
```


### Output


```bash
True
```


#### You Can See The Item Who Can EXIT From The Stack Using peek Or top


```python
from lstack import linkedStack

x = linkedStack([5, 6, 7], capacity=7, detail=True)
print(x.peek())
print(x.top())
```


### Output


```bash
7
7
```


#### You Can See How Many Items Are In The Stack Using len Function


```python
from lstack import linkedStack

x = linkedStack([5, 6, 7], capacity=7, detail=True)
print(len(x))
```


### Output


```bash
3
```


#### You Can Clear The Stack


```python
from lstack import linkedStack

x = linkedStack([5, 6, 7], capacity=7, detail=True)
print(x)
x.clear()
print(x)
```


### Output


```bash
╒════════════╕
│ ENTER  ^   │
│   |    |   │
│   v   EXIT │
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
│ 7          │
├────────────┤
│ 6          │
├────────────┤
│ 5          │
╘════════════╛
╒════════════╕
│ ENTER  ^   │
│   |    |   │
│   v   EXIT │
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
├────────────┤
╘════════════╛
```


### Note


The reason why it is called linkedStack is because this stack uses a non-circular doubly linked list


## License


This project is licensed under the MIT LICENSE - see the [LICENSE](https://opensource.org/licenses/MIT) for more details.
