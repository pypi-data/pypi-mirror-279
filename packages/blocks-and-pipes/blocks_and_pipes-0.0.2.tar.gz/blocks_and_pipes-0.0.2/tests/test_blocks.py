from collections.abc import Callable
from typing import Any

import pytest
from blocks_and_pipes.blocks import Block, CallableExhausted, CallableWithBlocks, CallableWithBlocksAndContext, MissingBlockSpecifications, blocks


class TestBlocks:
    def test_pure_python_block(self):
        def reduce(elements: list, init):
            def onMethod(fn):
                # the function "wrapper" takes the function `fn` ...
                carry = init
                for entry in elements:
                    # ... and executes it directly
                    carry = fn(carry, entry)
                reduce.result = carry # saves the result as function attribute
                # for a common decorator, a decorated function would be returned here,
                # but that is not necessary for our purposes
            return onMethod

        @reduce([1, 2, 3], 4)
        def add(sum, x):
            return sum + x
        assert reduce.result == 10

    def test_callable_object_block(self):
            class Reduce[ResultType, ValueType](CallableWithBlocks):
                # fn(carry, value) -> result
                callback: Block[[ResultType, ValueType], ResultType]
                result: ResultType

                def __call__(self, elements: list[ValueType], initial: ValueType|None = None):
                    self.elements = elements
                    self.initial = initial
                    return self.withResult(self.callback)

                def execute(self, callback):
                    if len(self.elements) == 0:
                        return self.initial
                    carry = self.initial if self.initial is not None else self.elements[0]
                    for entry in self.elements:
                        carry = callback(carry, entry)
                    return carry

            reduce = Reduce()
            @reduce([1, 2, 3, 4, 5], 6)
            def sum(carry, value):
                return carry + value
            assert reduce.result == 21

            assert reduce([1, 2, 3, 4, 5], 6)(lambda c, v: c + v + 1) == 26

    def test_function_blocks(self):
        def reduce(callback: Callable, elements: list[Any], initial: Any|None = None):
            if len(elements) == 0:
                return initial
            carry = initial if initial is not None else elements[0]
            for entry in elements:
                carry = callback(carry, entry)
            return carry

        red = blocks(reduce)
        @red(elements = [1, 2, 3, 4, 5], initial = 6).callback
        def sum(carry, value):
            return carry + value
        assert red.result == 21

    def test_multiple_blocks(self):
        class NestedCall(CallableWithBlocks):
            outer: Block[[int, int], int]
            nested: Block[[int], int]
            result: int

            def execute(self, outer, nested):
                return outer(nested(1), 2)

        callMe = NestedCall()

        @callMe.nested
        def divideBy2(number):
            return number / 2

        @callMe.outer
        def multiply(n1, n2):
            return n1 * n2

        assert callMe.result == 1.0

    def test_missing_block_exception(self):
        class NestedCall(CallableWithBlocks):
            outer: Block[[int, int], int]
            nested: Block[[int], int]
            result: int

            def execute(self, outer, nested):
                return outer(nested(1), 2)

        callMe = NestedCall()

        @callMe.nested
        def divideBy2(number):
            return number / 2

        with pytest.raises(MissingBlockSpecifications):
            callMe.result

    def test_context_and_blocks(self):
        class NestedCall(CallableWithBlocksAndContext):
            outer: Block[[int, int], int]
            nested: Block[[int], int]
            result: int

            def execute(self, outer, nested):
                return outer(nested(1), 2)

        with NestedCall() as callMe:
            @callMe.nested
            def divideBy2(number):
                return number / 2

            @callMe.outer
            def multiply(n1, n2):
                return n1 * n2

        with pytest.raises(CallableExhausted):
            callMe.result

        with pytest.raises(CallableExhausted):
            @callMe.nested
            def divideBy2(number):
                return number / 2
