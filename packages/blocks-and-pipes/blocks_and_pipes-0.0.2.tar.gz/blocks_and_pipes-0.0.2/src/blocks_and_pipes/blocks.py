from abc import abstractmethod
import collections.abc
import inspect
from typing import Any, Callable, ParamSpec, TypeVar, Union, get_args, get_origin


Parameters = ParamSpec('Parameters')
ReturnValue = TypeVar('ReturnValue')
Block = Callable[[Callable[Parameters, ReturnValue]], None]


class CallableExhausted(Exception):
    pass


class MissingBlockSpecifications(Exception):
    def __init__(self, missingBlocks):
        missingBlocks = ", ".join(missingBlocks)
        message = f"The follwing blocks were not specified: {missingBlocks}"
        super().__init__(message)


class BlockInternals:
    blocks: dict

    def __init__(self, source: dict|Any, ignoreUnresolved = False) -> None:
        if isinstance(source, dict):
            self.blocks = source
        else:
            self.blocks = {
                k: None
                for k in inspect.signature(source.execute).parameters.keys()
                if k != 'self'
                }
        self.exhausted = False
        self.ignoreUnresolved = ignoreUnresolved

    def isResolved(self):
        return all(self.blocks.values())

    def getMissingBlocks(self):
        return [block for block, clb in self.blocks.items() if clb is None]
        

class CallableWithBlocks:
    _block_internals: BlockInternals

    @abstractmethod
    def execute(self, *args: Any, **kwds: Any) -> Any:
        pass

    def __getattr__(self, name):
        if name in self._get_block_internals().blocks:
            def wrapper(fn):
                self._block_internals.blocks[name] = fn
                return self
            return wrapper

        raise AttributeError

    def _get_block_internals(self) -> BlockInternals:
        if '_block_internals' not in self.__dict__:
            self._block_internals = BlockInternals(self)
        return self._block_internals

    def _set_block_internals(self, internals: BlockInternals):
        self._block_internals = internals

    @property
    def result(self):
        if( not self._get_block_internals().ignoreUnresolved
            and not self._get_block_internals().isResolved() ):
            raise MissingBlockSpecifications(self._block_internals.getMissingBlocks())
        self._result = self.execute(**self._get_block_internals().blocks)
        return self._result

    def withSelf(self, block: Block):
        def wrapper(fn):
            block(fn)
            return self
        return wrapper

    def withResult(self, block: Block):
        def wrapper(fn):
            block(fn)
            return self.result
        return wrapper


class CallableWithBlocksAndContext(CallableWithBlocks):
    def __enter__(self):
        return self

    def __exit__(self, *_):
        self._get_block_internals().exhausted = True
        return False

    def __getattr__(self, name):
        if self._get_block_internals().exhausted:
            raise CallableExhausted("Context in which the Callable was valid has ended.")
        return super().__getattr__(name)

    @property
    def result(self):
        if self._get_block_internals().exhausted:
            raise CallableExhausted("Context in which the Callable was valid has ended.")
        return super().result

def blocks(clb: Callable):
    _blocks = {}
    _others = {}
    for name, param in inspect.signature(clb).parameters.items():
        is_callable = lambda ann: ann is Callable or ann is collections.abc.Callable
        if ( is_callable(param.annotation)
             or (get_origin(param.annotation) is Union
                 and any(map(is_callable, get_args(param.annotation)))) ):
            _blocks[name] = None
            if param.default is not inspect.Parameter.empty:
                _blocks[name] = param.default
            else:
                _blocks[name] = None
        else:
            _others[name] = param

    class CallableObject(CallableWithBlocks):
        def __call__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            return self

        def execute(self, **innerKwargs):
            innerKwargs = {**innerKwargs, **self.kwargs}
            return clb(*self.args, **innerKwargs)

    callableObj = CallableObject()
    callableObj._set_block_internals(BlockInternals(_blocks, True))

    return callableObj
