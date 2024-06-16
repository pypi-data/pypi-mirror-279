# Blocks and Pipes for Python

This package implements two somehow similar, but still different concepts.

- **Blocks:** This is an effort to create something **similar to Ruby blocks** in
  python, d.i. a method to easily specify **multiple multiline callbacks** as
  **arguments for a function**.
- **Pipes:** There are some pipe implementations for python already. This one
  aims to be **flexible, easily extendable** and also allows for specifying
  **multiline callbacks** as pipe operations.

If you are not interested in *blah-blah-blah*, just skip the rationale and head
straight for the [Usage and Examples](#usage-and-examples) Section.

## Installation

*TODO*

## Rationale

*TODO*

## Usage and Examples

### Blocks

#### Blocks with pure Python

(Ruby) Blocks can be emulated in Python easily even without this package. The
trick is to use function decorators, which execute the decorated function
directly:
```python
# take an input `elements` list and return a function wrapper.
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
print(reduce.result) # get the result from the function attribute
# outputs: 10
```

This is already a quite elegant solution. The `blocks_and_chain` package just
adds a bit of sugar and allowes for multiple blocks to be injected.

#### Blocks with this Library

Let's first take the pure Python example and reimplement it using the *Blocks and
Pipes* library.
```python
from blocks_and_pipes import CallableWithBlocks, Block
# other imports from standard lib are skipped

class Reduce[ResultType, ValueType](CallableWithBlocks):
    # fn(carry, value) -> result
    callback: Block[[ResultType, ValueType], ResultType]
    result: ResultType

    def init(self, elements: list[ValueType], initial: ValueType|None = None):
        self.elements = elements
        self.initial = initial
        return self.callback

    def __call__(self, callback):
        carry = self.initial if self.initial is not None else self.elements[0]
        for entry in self.elements:
            carry = callback(carry, entry)
        return carry

reduce = Reduce()
@(reduce.init([1, 2, 3], 4))
def add(sum, x):
    return sum + x
print(reduce.result)
```

Type hinting is not strictly necessary, but it is a nice addition. Firstly it
will satisfy the type-checker and secondly it will document the desired
parameters and return values of your blocks and the result after calling the
callable.

**Remarks:**
- To implement the "Callable" you must obviously implement the `__call__`
  method of the object to be callable.
- The `__call__` method should only take the injected callbacks as arguments.
  Any other input must be injected using other means (e.g. the `init`-method in
  the example).
- The parameter names of the `__call__`-method should match the names of the
  declared blocks (here we have the parameter `callback`), otherwise the
  type-checker will not be able to check the type-correctnes of the later on
  defined blocks.
- The types of the declared blocks are **not** `Callable`, but `Block`, because
  we declare the type of the wrapper function here
  (see [Blocks with pure Python](#blocks-with-pure-python)), for which `Block`
  is just an alias.

Now defining simple functions with blocks using this library might be a bit of
overkill. The pure python version, although a bit more cryptic, may rather be
your taste. It gets a bit more exciting, when using a Callable with several
blocks, which is easily possible.

Also, if you like, you can use a Callable inside a managed context, which will
prohibit later usage or modification of the Callable.

```python
class NestedCall(CallableWithBlocksAndContext):
    outer: Block[[int, int], int]
    nested: Block[[int], int]
    result: int

    def __call__(self, outer, nested):
        return outer(nested(1), 2)

with NestedCall() as callMe:
    @callMe.nested
    def divideBy2(number):
        return number / 2

    # raises MissingBlockSpecifications
    # print(f"The result is {callMe.result}")

    @callMe.outer
    def multiply(n1, n2):
        return n1 * n2

    print(f"The result is {callMe.result}.")
    # The result is 1.0.

# raises CallableExhausted
#@callMe.blockZero
#def addNumbers3(a, b: float):
#    return a + b

# raises CallableExhausted
#print(f"result is now {callMe.result}")
```

### Pipes

#### Intro

Pipes in their simplest form can be used like that:

```python
from blocks_and_pipes import Pipe
# ... other imports

pipe = Pipe[Iterable[int], Iterable[int]](range(10))

@pipe.append
def onlyOdd(iterable):
    return itertools.filterfalse(lambda num: num % 2 == 0, iterable)

@pipe.append
def firstNumberBiggerThan4(iterable):
    return itertools.dropwhile(lambda num: num <= 4, iterable)

print(list(pipe.exec()))
# [5, 7, 9]
```

This is not very useful yet, although it shows some basic principles. Note, that
the Typehints are not needet, but it helps the Type-Checker to check against
input and output type of the pipe (here both are `Iterable[int]`).

#### Extending the standard Pipe

To have this become a bit more useful, You can subclass the `Pipe`-class and add
some pipe functions. By default only a very limited set of functions exist,
namely `append` (we have seen that already) and the special functions
`recurseIntoDictValues` and `recurseIntoIterable`. - Also You should not
overwrite the other methods from the `Pipe`-class without knowing what You do
;).

As an example take the following class as a start. You may want to extend it for
your Purposes later:

```python

Input = TypeVar('Input')
Output = TypeVar('Output')

class IterPipe(Pipe[Input, Output]):
    def filterfalse(self, callback: Callable[[Any], bool]):
        def filterfalse(iterable):
            return itertools.filterfalse(callback, iterable)
        return self.append(filterfalse)

    def filter(self, callback: Callable[[Any], bool]):
        # a bit more concise using partial
        return self.append(partial(filter, callback))

    def dropwhile(self, callback: Callable[[Any], bool]):
        return self.append(partial(itertools.dropwhile, callback))

    def takewhile(self, callback: Callable[[Any], bool]):
        return self.append(partial(itertools.takewhile, callback))

    # if additional parameters (here the initializer argument for reduce) shall
    # be specified, an additional wrapper function must be implemented
    def reduce(self, initializer=object()):
        def reduceByCallback(callback: Callable):
            # a hack to determine, if the initializer argument was passed by
            # the user or is just the default value
            if initializer is self.reduce.__defaults__[0]:
                self.append(lambda iterable: reduce(callback, iterable))
            else:
                self.append(lambda iterable: reduce(callback, iterable, initializer))
            return self
        return reduceByCallback
```

Remark the Generic `Input` and `Output` parameters, which will enable You later
to specify type-hints for your input and output type.

#### Different Styles for creating the Pipe

This class can now be used instead of the default Pipe class:
```python
@(pipe := IterPipe[Iterable[int], int](range(20))).filter
def onlyOdd(num):
    return num % 2 == 0

@pipe.reduce(10)
def sum(carry, x):
    return carry + x

print(pipe.exec())
# 100
```

Alternatively, You can call it like that:
```python
result = ((IterPipe(range(20))).filter(lambda num: num % 2 == 0)
                               .reduce(10)(lambda carry, x: carry + x)
                               .exec())
print(result)
# 100
```

Mixed Variants are possible:
```python
pipe = IterPipe()

@pipe.filter
def onlyOdd(num):
    return num % 2 == 0

print(pipe.reduce()(lambda carry, x: carry + x).exec(range(20)))
# 90
```

#### Reusing Pipes / Continuing Usage after Execution

By default Pipes can be reused as often as You like to after their definition.
```python
pipe = IterPipe(range(20))
pipe.filter(lambda num: num % 2 == 0)
print(list(pipe.exec()))
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
print(list(pipe.exec(10)))
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

When using the special `memorize`-Parameter to the exec-call. The result is
stored in the pipe and will be reused as input in subsequent calls (otherwise
the input is always the input lastly specified).
```python
pipe = IterPipe(range(20))
pipe.filter(lambda num: num % 2 == 0)
# memorize the result as input for subsequent executions
result = pipe.append(lambda x: list(x)).exec(range(10), memorize=True)
print(result)
# [0, 2, 4, 6, 8]
print(pipe.reduce()(lambda carry, x: carry + x).exec())
# 20
```

The pipe can be `reset`, meaning, that the all existing callbacks will be
removed.
```python
pipe = IterPipe(range(10))
pipe.filter(lambda num: num % 2 == 0)
print(pipe.exec())
# [0, 2, 4, 6, 8]
pipe.reset()
print(pipe.exec())
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

#### Advanced Features: Recursing into Dictionaries / Iterables

If you have nested dictionaries / lists, you can recurse into them, which will
automatically create a subpipe on these lists / dictionaries.

```python
from collections import Counter

itemsInStore = { 'storehouse1': ['apple', 'pear', 'pear'],
                 'storehouse2': ['mushroom', 'mushroom', 'mario'] }

with IterPipe[dict[str, list[str]], dict](itemsInStore) as pipe:
    @pipe.recurseIntoDictValues()
    def countByName(subpipe: IterPipe):
        @subpipe.append
        def countByName(items: Iterable[str]):
            return Counter(items)

    pprint.pprint(dict(pipe.exec()))
# {'storehouse1': Counter({'pear': 2, 'apple': 1}),
#  'storehouse2': Counter({'mushroom': 2, 'mario': 1})}
```

This can be done arbitrarily often.
```python
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

    @subpipe.append
    def printWorld(world: dict):
        print(f"Name: {world['name']}")
        print(f"Average Inhabitants: {world['avgInhabitants']}")

pipe.exec()
# Name: snowflake
# Average Inhabitants: 40.333333333333336
# Name: pythonplanet
# Average Inhabitants: 72.0
```
