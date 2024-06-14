# pretty_assert

English | [简体中文](./README.zh-CN.md)

Prints pretty, **user friendly** assert messages.

![ex](./static/eq_example.png)

## Features

- Do not print traces that confuse the user
- Add Comment
- Customize colors and other options
- `assert_eq` enhancement with icdiff

## Installation

```sh
pip install pretty-assert
```

## Usage

```python
from pretty_assert import (
    init,
    assert_,
    assert_eq,
    assert_ge,
    assert_gt,
    assert_in,
    assert_le,
    assert_lt,
    assert_ne,
    assert_not_in,
)
some_bool = True
some_number = 1
assert_(some_bool)  # you can assert without comment
assert_(some_bool, "some_bool is not True")
assert_eq(some_number, 1, "some_number is not 1")
...
```

For more usage and customization, please check out [examples](./examples/).

## Thanks

- [assert2](https://crates.io/crates/assert2): inspired by
- [pytest-icdiff](https://github.com/hjwp/pytest-icdiff): code reference
