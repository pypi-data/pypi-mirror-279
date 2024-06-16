import copy
from functools import partial
from typing import Callable, Generic, Iterable, TypeVar, Self


class PipeExhausted(Exception):
    pass


Input = TypeVar('Input')
Output = TypeVar('Output')


class Pipe(Generic[Input, Output]):
    def __init__(self, input: Input|None = None, *args, **kwargs) -> None:
        self._pipe = []
        self._input = input
        self.exausted = False
        self.args = args
        self.kwargs = kwargs

    def input(self, input: Input|None):
        self._input = input
        return self

    def getChain(self):
        pipe = copy.copy(self._pipe)
        def chained(input, *args, **kwargs):
            if len(pipe) == 0:
                return input
            input = pipe[0](input, *args, **kwargs)
            for f in pipe[1:]:
                input = f(input)
            return input
        return chained

    def reset(self):
        self._pipe = []
        return self

    def exec(self, input: Input|None = None, reset=False, memorize=False) -> Output:
        result = self._exec(input)
        if memorize:
            self._input = result
        if reset:
            self.reset()
        return result

    def _exec(self, input: Input|None = None, *args, **kwargs):
        if self.exausted:
            raise PipeExhausted("Context in which the Pipe was valid has ended.")
        args = args or self.args
        kwargs = kwargs or self.kwargs
        result = self._input if input is None else input
        if len(self._pipe) == 0:
            return result # pyright: ignore
        result = self._pipe[0](result, *args, **kwargs)
        for f in self._pipe[1:]:
            result = f(result)
        return result # pyright: ignore

    def append(self, callback: Callable):
        self._pipe.append(callback)
        return self

    def recurseIntoDictValues(self, withKey = False):
        def recurse(callback: Callable[[Self], None]):
            subpipe = self.__class__()
            callback(subpipe)
            if withKey:
                def mapDictValues(f: Callable, d: dict):
                    return {k: f(k, v) for k, v in d.items()}
            else:
                def mapDictValues(f: Callable, d: dict):
                    return {k: f(v) for k, v in d.items()}
            return self.append(partial(mapDictValues, subpipe.getChain()))
        return recurse

    def recurseIntoIterable(self, callback: Callable[[Self], None]):
        subpipe = self.__class__()
        callback(subpipe)
        def mapValues(f: Callable, it:Iterable):
            return [f(item) for item in it]
        return self.append(partial(mapValues, subpipe.getChain()))

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.exausted = True
        return False
