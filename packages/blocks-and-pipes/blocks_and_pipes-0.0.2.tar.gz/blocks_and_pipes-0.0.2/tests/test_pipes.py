import pytest
from collections.abc import Callable, Iterable
from typing import Any, TypeVar
from blocks_and_pipes import Pipe
import itertools
from functools import partial, reduce

from blocks_and_pipes.pipes import PipeExhausted

Input = TypeVar('Input')
Output = TypeVar('Output')

class IterPipe(Pipe[Input, Output]):
    def filter(self, predicate: Callable[[Any], bool]):
        return self.append(partial(filter, predicate))

    def filterfalse(self, predicate: Callable[[Any], bool]):
        return self.append(partial(itertools.filterfalse, predicate))

    def dropwhile(self, predicate: Callable[[Any], bool]):
        return self.append(partial(itertools.dropwhile, predicate))

    def takewhile(self, predicate: Callable[[Any], bool]):
        return self.append(partial(itertools.takewhile, predicate))

    def reduce(self, initializer=object()):
        def reduceByCallback(callback: Callable[[Any, Any], Any]):
            if initializer is self.reduce.__defaults__[0]:
                self.append(lambda iterable: reduce(callback, iterable))
            else:
                self.append(lambda iterable: reduce(callback, iterable, initializer))
            return self
        return reduceByCallback

class TestPipe:
    def test_bare_pipe(self):
        pipe = Pipe[Iterable[int], Iterable[int]](range(10))

        @pipe.append
        def onlyOdd(iterable):
            return itertools.filterfalse(lambda num: num % 2 == 0, iterable)

        @pipe.append
        def firstNumberBiggerThan4(iterable):
            return itertools.dropwhile(lambda num: num <= 4, iterable)

        assert list(pipe.exec()) == [5, 7, 9]

    def test_normal_style(self):
        pipe = IterPipe[Iterable[int], int](range(20))
        @pipe.filter
        def onlyOdd(num):
            return num % 2 == 0

        @pipe.reduce(10)
        def sum(carry, x):
            return carry + x

        assert pipe.exec() == 100

    def test_concise_style(self):
        result = (IterPipe[Iterable[int], int](range(20))
          .filter(lambda num: num % 2 == 0)
          .reduce(10)(lambda num, x: num + x)
          .exec())
        assert result == 100

    def test_mixed_style(self):
        pipe = IterPipe[Iterable[int], int](range(20))
        @pipe.filter
        def onlyOdd(num):
            return num % 2 == 0

        pipe.dropwhile(lambda x: x < 10)

        @pipe.reduce()
        def sum(carry, x):
            return carry + x

        assert pipe.exec() == 70

    def test_pipe_reusage_no_change(self):
        pipe = IterPipe(range(20))
        pipe.filter(lambda num: num % 2 == 0)
        result1 = list(pipe.exec())
        result2 = list(pipe.exec())
        assert result1 == result2

    def test_pipe_reusage_new_input(self):
        pipe = IterPipe(range(20))
        pipe.filter(lambda num: num % 2 == 0)
        result1 = list(pipe.exec())
        assert result1 == [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        result2 = list(pipe.exec(range(10)))
        assert result2 == [0, 2, 4, 6, 8]

    def test_pipe_memorize(self):
        pipe = IterPipe(range(20))
        pipe.filter(lambda num: num % 2 == 0)
        pipe.append(lambda x: list(x))
        pipe.exec(range(10), memorize=True)
        assert pipe.reduce()(lambda carry, x: carry + x).exec() == 20

    def test_pipe_reset(self):
        pipe = IterPipe(range(10))
        pipe.filter(lambda num: num % 2 == 0)
        assert list(pipe.exec()) == [0, 2, 4, 6, 8]
        pipe.reset()
        assert list(pipe.exec()) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_managed_context_for_pipe(self):
        with IterPipe(range(10)) as pipe:
            pipe.filter(lambda num: num % 2 == 0)
            pipe.exec()
        with pytest.raises(PipeExhausted):
            pipe.filterfalse(lambda num: num % 3 == 0)
        with pytest.raises(PipeExhausted):
            pipe.exec()

    def test_recurse_into_dict(self):
        from collections import Counter

        itemsInStore = { 'storehouse1': ['apple', 'pear', 'pear'],
                         'storehouse2': ['mushroom', 'mushroom', 'mario'] }

        pipe = IterPipe[dict[str, list[str]], dict](itemsInStore)
        @pipe.recurseIntoDictValues()
        def countByName(subpipe: IterPipe):
            @subpipe.append
            def countByName(items: Iterable[str]):
                return Counter(items)

        assert pipe.exec() == {'storehouse1': Counter({'pear': 2, 'apple': 1}),
                               'storehouse2': Counter({'mushroom': 2, 'mario': 1})}

    def test_complex_recurse(self):
        tinyWorlds = [ {'name': 'snowflake', 'inhabitants': {2019: 22, 2020: 50, 2021: 49}},
               {'name': 'pythonplanet', 'inhabitants': {2018: 44, 2022: 100}} ]

        pipe = IterPipe(tinyWorlds)

        @pipe.recurseIntoIterable
        def mapWorld(subpipe: IterPipe):
            @subpipe.append
            def copyKey(world: dict):
                world['avgInhabitants'] = world['inhabitants']
                return world

            @subpipe.recurseIntoDictValues(withKey=True)
            def mapInhabitants(subsubpipe: IterPipe):
                @subsubpipe.append
                def averageInhabitants(key, value):
                    if key == 'avgInhabitants':
                        return sum(value.values())/len(value.values())
                    return value

        assert pipe.exec() == [ {'avgInhabitants': 40.333333333333336,
                                 'inhabitants': {2019: 22, 2020: 50, 2021: 49},
                                 'name': 'snowflake'},
                                {'avgInhabitants': 72.0, 
                                 'inhabitants': {2018: 44, 2022: 100},
                                 'name': 'pythonplanet'} ]
