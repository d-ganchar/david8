# david8

`david8` is a lightweight Python SQL builder with zero dependencies.
Clean API. Safe parameters. No ORM magic.

No manual parameter naming. Just pass values - `david8` handles the rest:

    .where(eq('age', 18), lt('score', 100))
    # WHERE age = %(p1)s AND score < %(p2)s
    # {'p1': 18, 'p2': 100}

100% test coverage · thousands of downloads

Built-in dialect support: ClickHouse · DuckDB · PostgreSQL · Apache Doris · MySQL · SQLite

See [Wiki](https://github.com/d-ganchar/david8/wiki)