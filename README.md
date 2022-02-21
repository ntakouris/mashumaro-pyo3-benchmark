# mashumaro-pyo3-benchmarks

Sometimes the overhead of calling C/CPP/Rust python bindings is greater than using an efficient python library.
Here are some [Fatal1ty/mashumaro](https://github.com/Fatal1ty/mashumaro) equivalent benchmarks leveraging pyo3 bindings instead of
other python libraries.

* This repo is compatible with VSCode's dev-container format.

You can install `schema_rs` by `cd schema_rs && pip3 install .`

## Implementation Details

Here are the schema in python (equivalents in rust-pyo3 bindings are under `schema_rs`)

```py
from enum import Enum
from typing import List
from dataclasses import dataclass
from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.mixins.msgpack import DataClassMessagePackMixin

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"

@dataclass
class CurrencyPosition(DataClassJSONMixin, DataClassMessagePackMixin):
    currency: Currency
    balance: float

@dataclass
class StockPosition(DataClassJSONMixin, DataClassMessagePackMixin):
    ticker: str
    name: str
    balance: int

@dataclass
class Portfolio(DataClassJSONMixin, DataClassMessagePackMixin):
    currencies: List[CurrencyPosition]
    stocks: List[StockPosition]

my_portfolio = Portfolio(
    currencies=[
        CurrencyPosition(Currency.USD, 238.67),
        CurrencyPosition(Currency.EUR, 361.84),
    ],
    stocks=[
        StockPosition("AAPL", "Apple", 10),
        StockPosition("AMZN", "Amazon", 10),
    ]
)

msgpack_bytes = my_portfolio.to_msgpack()
json_str = my_portfolio.to_json()

Portfolio.from_msgpack(msgpack_bytes)
Portfolio.from_json(json_str)
```

With the rust bindings provided, you can achieve similar semantics (check `demonstration.py`):

```py
import schema_rs

my_portfolio_rs = schema_rs.Portfolio(
    currencies=[
        schema_rs.CurrencyPosition(schema_rs.Currency("USD"), 238.67),
        schema_rs.CurrencyPosition(schema_rs.Currency("EUR"), 361.84),
    ],
    stocks=[
        schema_rs.StockPosition("AAPL", "Apple", 10),
        schema_rs.StockPosition("AMZN", "Amazon", 10),
    ],
)

msgpack_bytes = my_portfolio_rs.to_msgpack()
json_str = my_portfolio_rs.to_json()

Portfolio.from_msgpack(my_portfolio_rs)
Portfolio.from_json(my_portfolio_rs)
```

## Benchmark Results

On some average Ryzen 5 desktop (`python3 benchmarks.py`):

```txt
mashumaro(to_json):      9.238211507999949e-06
pyo3(to_json):           0.6136147130000609

mashumaro(to_msgpack):   7.3272712759999195
pyo3(to_msgpack):        7.3272712759999195

mashumaro(from_json):    1.1536665370000265e-05
pyo3(from_json):         1.0166272180003944

mashumaro(from_msgpack): 11.083359452999503
pyo3(from_msgpack):      0.974420227000337
```
