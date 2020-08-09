import inspect
from inspect import signature
import pydoc
import inspect
from types import FunctionType, ModuleType
from typing import Dict, List, Optional
import docstring_parser
import dataclasses
from docstring_parser.common import Docstring
from loguru import logger


def get_example_code(doc: Docstring) -> Optional[str]:
    for meta in doc.meta:
        if any(a.lower() in {"example", "examples"} for a in meta.args):
            return meta.description


@dataclasses.dataclass
class Routine:
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    signature: Optional[inspect.Signature] = None
    example_code: Optional[str] = None

    @classmethod
    def from_obj(cls, obj: FunctionType) -> "Routine":
        docstring = inspect.getdoc(obj)
        doc = docstring_parser.parse(docstring) if docstring else None
        short_description = doc.short_description.strip() if doc else None
        long_description = doc.long_description.strip() if doc else None
        try:
            signature = inspect.signature(obj)
        except ValueError:
            signature = None
        return cls(
            name=obj.__name__,
            short_description=short_description,
            long_description=long_description,
            signature=signature,
        )


@dataclasses.dataclass
class Module:
    name: str
    modules: Dict[str, "Module"] = dataclasses.field(default_factory=dict)
    functions: Dict[str, Routine] = dataclasses.field(default_factory=dict)

    @classmethod
    def from_obj(cls, name: str, obj: ModuleType) -> "Module":
        assert name
        functions = {
            name: Routine.from_obj(fn)
            for (name, fn) in inspect.getmembers(obj, inspect.isroutine)
        }
        return cls(name=name, functions=functions)

    @classmethod
    def from_file(cls, path: str) -> "Module":
        mod = pydoc.importfile(path)
        obj, name = pydoc.resolve(mod) or (None, "")
        assert isinstance(obj, ModuleType)
        logger.info(f"Load {name}")
        return cls.from_obj(name, obj)

