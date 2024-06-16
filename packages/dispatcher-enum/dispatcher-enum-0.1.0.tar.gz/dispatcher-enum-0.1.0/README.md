# ͱ Start with the "why" 


Consider this config file:
```yaml
aggregation: mean
```

## Not good

```py
from numpy import mean, median
import yaml

config = yaml.safe_load('aggregation: mean')
runner = eval(config['aggregation']) # OUCH executable YAML
```

## Much better, but still hella wobbly

```py
import numpy as np, yaml

dispatcher = {"mean": np.mean, "median": np.median}

config = yaml.safe_load('aggregation: mean')
runner = dispatcher[config['aggregation']]
```

## Tidier

```py
import numpy as np, yaml
from pydantic import BaseModel, field_validator

dispatcher = {"mean": np.mean, "median": np.median}

class Config(BaseModel):
    aggregation: str

    @field_validator('aggregation')
    @classmethod
    def agg_must_be_valid(cls, v: str) -> str:
        if v not in dispatcher:
            raise ValueError('Invalid aggregation')
        return v.title()

config = Config(yaml.safe_load('aggregation: mean'))
runner = dispatcher[config.aggregation]
```

## Very much better
```py
import numpy as np, yaml
from pydantic import BaseModel
from dispatcher import Dispatcher

# shortcut utility that creates a DispatchEnum object
Aggregation = Dispatcher(
    mean = np.mean,
    median = np.median
)
class Config:
    aggregation: Aggregation = Aggregation.MEAN

config = Config(yaml.safe_load('aggregation: mean'))

runner = config.aggregation # ding
# now the "aggregation" YAML field is parsed by pydantic into 
# an Aggregation object derived from an Enum that's also callable!
runner0 = lambda xs: config.aggregation(xs) # ding ding ding ding.
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

config = Parser({"check_parity": "odd" })
print(config.check_parity) # prints Parity.ODD
```

With `DispatchEnum` we're able to assign an additional property to each Enum member:

```py
class Parity(DispatchEnum):
    ODD = "odd"
    EVEN = "even"

Parity.assign(Parity.ODD, lambda x: x % 2 == 1)
Parity.assign(Parity.EVEN, lambda x: x % 2 == 0)
# or
Parity.from_dict({"ODD": lambda x: x % 2 == 1, "EVEN": lambda x: x % 2 == 0})

print(Parity.ODD(2)) # prints False
```

Therefore `DispatchEnum`is both a "dispatcher" (mapping a string identifier to a function)
and an `Enum` (enabling Pydantic goodness).

For further convenience, the `Dispatcher` function creates a DispatchEnum filling in member names:

```py
Aggregation = Dispatcher(
    mean = np.mean,
    median = np.median
)
# does the same as 

class Aggregation(DispatchEnum):
    MEAN: "mean"
    MEDIAN: "median"
Aggregation.from_dict({"mean": np.mean, "median": np.median})
```

# Installation

Right now you should download `dispatch.py` and vendor it in. Soonishly a more mature
version will be hitting PyPI too.