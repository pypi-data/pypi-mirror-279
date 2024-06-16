from abc import abstractmethod
import inspect
from typing import Any, Callable, ParamSpec, TypeVar


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
    def __init__(self, blocksObject) -> None:
        self.blocks = {
            k: None
            for k in inspect.signature(blocksObject.__call__).parameters.keys()
            if k != 'self'
            }
        self.exhausted = False

    def isResolved(self):
        return all(self.blocks.values())

    def getMissingBlocks(self):
        return [block for block, clb in self.blocks.items() if clb is None]
        

class CallableWithBlocks:
    _block_internals: BlockInternals

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

    def __getattr__(self, name):
        if name in self._get_block_internals().blocks:
            def wrapper(fn):
                self._block_internals.blocks[name] = fn
            return wrapper

        raise AttributeError

    def _get_block_internals(self) -> BlockInternals:
        if '_block_internals' not in self.__dict__:
            self._block_internals = BlockInternals(self)
        return self._block_internals

    @property
    def result(self):
        if not self._get_block_internals().isResolved():
            raise MissingBlockSpecifications(self._block_internals.getMissingBlocks())
        self._result = self(**self._get_block_internals().blocks)
        return self._result


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
        if self._block_internals.exhausted:
            raise CallableExhausted("Context in which the Callable was valid has ended.")
        return super().result
