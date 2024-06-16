# ͱ Start with the "why" 

DispatchEnum is *the* Pythonic way to deal with the "strategy in config" pattern, where
we want choices in implementation details ("strategies") to be available outside 
Python code proper.

Consider this cfg file:
```yaml
aggregation: mean
length: square
```

We see this typically when we want to allow for different aggregating functions (mean, median...) to be
used in a functionality that meaningfully accepts them.

## Not good

```py
from numpy import mean, median, abs # rock the global namespace!
import yaml

square = lambda x: x*x

def excess(lst, cfg):
    agg = eval(cfg['aggregation'])(lst) # OUCH executable YAML
    return [eval(cfg['length'])(val - agg) for val in lst] # OOF right in the feels

cfg = yaml.safe_load(config.yaml)
print(excess([1,2,3], cfg)) # prints [1,0,1] 
```

## Much better, but still hella wobbly

```py
import numpy as np, yaml

agg_dispatcher = {"mean": np.mean, "median": np.median}
len_dispatcher = {"square": lambda x: x*x, "abs": np.abs}

def excess(lst, cfg):
    agg = agg_dispatcher[cfg['aggregation']](lst)
    return [len_dispatcher[cfg['length']](val - agg) for val in lst]
cfg = yaml.safe_load(config.yaml)
print(excess([1,2,3], cfg)) # same as above 
```

## Safer with Pydantic but drowning in boilerplate

```py
import numpy as np, yaml
from pydantic import BaseModel, field_validator

agg_dispatcher = {"mean": np.mean, "median": np.median}
len_dispatcher = {"square": lambda x: x*x, "abs": np.abs}

class Config(BaseModel):
    aggregation: str
    length: str

    @field_validator('aggregation')
    @classmethod
    def agg_must_be_valid(cls, v: str) -> str:
        if v not in agg_dispatcher:
            raise ValueError('Invalid aggregation')
        return v

    @field_validator('length')
    @classmethod
    def len_must_be_valid(cls, v: str) -> str:
        if v not in len_dispatcher:
            raise ValueError('Invalid length')
        return v

def excess(lst, cfg):
    agg = agg_dispatcher[cfg.aggregation](lst)
    return [len_dispatcher[cfg.length](val - agg) for val in lst]

cfg = yaml.safe_load(config.yaml)
print(excess([1,2,3], cfg)) # same as above 

```

## Class and quality
```py
import numpy as np, yaml
from pydantic import BaseModel
from dispatcher import Dispatcher

# shortcut utility that creates a DispatchEnum object
AggregationStrategy = Dispatcher(
    mean = np.mean,
    median = np.median
)
LengthStrategy = Dispatcher(
    square = lambda x: x*x,
    abs = np.abs
) 
class Config:
    aggregation: AggregationStrategy = AggregationStrategy.MEAN
    length:  LengthStrategy 

cfg = Config(yaml.safe_load(config.yaml))
def excess(lst, cfg):
    agg = cfg.aggregation(lst)   # ding ding ding ding
    return [cfg.length(val - agg) for val in lst]

```

# The "what"

This code provides a `DispatchEnum` class that subclasses from Enum but holds an
additional value for each member. This is most useful in combination with Pydantic,
which is able to parse Enum-valued fields received as strings, i.e.

```py
class Parity(Enum):
    ODD = "odd"
    EVEN = "even"

class Parser(BaseModel):
     check_parity: Parity

cfg = Parser({"check_parity": "odd" })
print(cfg.check_parity) # prints Parity.ODD
```

With `DispatchEnum` we're able to assign an additional property to each Enum member:

```py
class Parity(DispatchEnum):
    ODD = "odd"
    EVEN = "even"

Parity.from_dict({"ODD": lambda x: x % 2 == 1, "EVEN": lambda x: x % 2 == 0})
print(Parity.ODD(2)) # prints False
```

Therefore `DispatchEnum`is both a "dispatcher" (mapping a string identifier to a function)
and an `Enum` (enabling Pydantic goodness).

For further convenience, the `Dispatcher` function creates a DispatchEnum filling in member names:

```py
AggregationStrategy = Dispatcher(
    mean = np.mean,
    median = np.median
)
```
which is shorthand for 
```py
class AggregationStrategy(DispatchEnum):
    MEAN: "mean"
    MEDIAN: "median"
AggregationStrategy.from_dict({"mean": np.mean, "median": np.median})
```

# Installation

Right now you should download `dispatch.py` and vendor it in. Soonishly a more mature
version will be hitting PyPI too.