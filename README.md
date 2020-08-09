# pydoc-md: Generate API document from python files

- [x] Generate API document from Python files
- [x] Support stub files - automatically detect stubs and merge the results.

## Usage

```console
$ pip install pydoc-md
$ pydoc-md foo.py

### `add`

```python
def add(a: int, b: int) -> int: ...
```

Foo bar baz

Adds two integers and returns it

```python
>>> add(1, 2)
3
```
```