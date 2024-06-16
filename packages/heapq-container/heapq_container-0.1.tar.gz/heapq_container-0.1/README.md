# heapq-container

[![PyPI](https://img.shields.io/pypi/v/heapq-container.svg)](https://pypi.org/project/heapq-container/)
[![Tests](https://github.com/lonnen/heapq-container/actions/workflows/test.yml/badge.svg)](https://github.com/lonnen/heapq-container/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/lonnen/heapq-container?include_prereleases&label=changelog)](https://github.com/lonnen/heapq-container/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/lonnen/heapq-container/blob/main/LICENSE)

a Container datatype wrapper for the Python standard library heapq module.

## Installation

Install this library using `pip`:
```bash
pip install heapq-container
```
## Usage

```python

from heapqueue import HeapQueue

 def heapsort(iterable):
    h = HeapQueue(iterable)
    return [h.pop() for _ in range(len(h))]

heapsort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])
# -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd heapq-container
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
