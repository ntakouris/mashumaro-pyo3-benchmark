import schema
import schema_rs

import json
from functools import partial

if __name__ == "__main__":
    my_portfolio = schema.Portfolio(
        currencies=[
            schema.CurrencyPosition(schema.Currency.USD, 238.67),
            schema.CurrencyPosition(schema.Currency.EUR, 361.84),
        ],
        stocks=[
            schema.StockPosition("AAPL", "Apple", 10),
            schema.StockPosition("AMZN", "Amazon", 10),
        ],
    )

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

    no_spaces_encoder = partial(json.dumps, separators=(",", ":"))
    json_py = my_portfolio.to_json(encoder=no_spaces_encoder).strip()
    json_rs = my_portfolio_rs.to_json()

    print(json_py)
    print(json_rs)

    assert json_py == json_rs
