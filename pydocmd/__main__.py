from fire import Fire
from .parser import Module
from .generator import gen


def main(path: str):
    mod = Module.from_file(path)
    print(gen(mod))


if __name__ == "__main__":
    Fire(main)
