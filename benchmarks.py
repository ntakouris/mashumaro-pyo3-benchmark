import timeit


import schema
import schema_rs

if __name__ == "__main__":
    loop_times = 1_000_000

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

    # mashumaro -> json
    mashumaro_to_json = (
        timeit.timeit("my_portfolio.to_json()", globals=globals(), number=loop_times)
        / loop_times
    )

    # json -> mashumaro
    json_payload = my_portfolio.to_json()
    mashumaro_from_json = (
        timeit.timeit(
            "schema.Portfolio.from_json(json_payload)",
            globals=globals(),
            number=loop_times,
        )
        / loop_times
    )

    # pyo3 -> json
    pyo3_to_json = timeit.timeit(
        "my_portfolio_rs.to_json()", globals=globals(), number=loop_times
    )

    # json -> pyo3
    json_payload = my_portfolio_rs.to_json()
    pyo3_from_json = timeit.timeit(
        "schema_rs.Portfolio.from_json(json_payload)",
        globals=globals(),
        number=loop_times,
    )

    # mashumaro -> msgpack
    mashumaro_to_msgpack = timeit.timeit(
        "my_portfolio.to_msgpack()", globals=globals(), number=loop_times
    )

    # msgpack -> mashumaro
    msgpack_payload = my_portfolio.to_msgpack()
    mashumaro_from_msgpack = timeit.timeit(
        "schema.Portfolio.from_msgpack(msgpack_payload)",
        globals=globals(),
        number=loop_times,
    )

    # pyo3 -> msgpack
    pyo3_to_msgpack = timeit.timeit(
        "my_portfolio_rs.to_msgpack()", globals=globals(), number=loop_times
    )

    # msgpack -> pyo3
    msgpack_payload = my_portfolio_rs.to_msgpack()
    pyo3_from_msgpack = timeit.timeit(
        "schema_rs.Portfolio.from_msgpack(msgpack_payload)",
        globals=globals(),
        number=loop_times,
    )

    print(
        f"""
        mashumaro(to_json):      {mashumaro_to_json}
        pyo3(to_json):           {pyo3_to_json}

        mashumaro(to_msgpack):   {mashumaro_to_msgpack}
        pyo3(to_msgpack):        {pyo3_to_msgpack}

        mashumaro(from_json):    {mashumaro_from_json}
        pyo3(from_json):         {pyo3_from_json}

        mashumaro(from_msgpack): {mashumaro_from_msgpack}
        pyo3(from_msgpack):      {pyo3_from_msgpack}
    """
    )
