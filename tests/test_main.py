from pydoc_md.__main__ import _main
from pathlib import Path

EXPECTED = """### `add`

```python
def add(a: int, b: int) -> int: ...
```

Foo bar baz

Adds two integers and returns it

```python
>>> add(1, 2)
3
```

"""


def test_main(tmp_path):
    output_path = tmp_path / "foo.md"
    _main(Path(__file__).parent / "foo/__init__.py", output_path)
    assert EXPECTED == output_path.read_text()

