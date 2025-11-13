def run_david8():
    from .simple_select_david8 import generate_sql
    generate_sql()

def run_sqlalchemy():
    from .simple_select_david8 import generate_sql
    generate_sql()

def run_pypika():
    from .simple_select_pypika import generate_sql
    generate_sql()

def run_peewee():
    from .simple_select_peewee import generate_sql
    generate_sql()


ROUNDS = 20
ITERATIONS = 1000


def test_david8(benchmark):
    benchmark.pedantic(
        lambda : run_david8(),
        rounds=ROUNDS,
        iterations=ITERATIONS
    )

def test_sqlalchemy(benchmark):
    benchmark.pedantic(
        lambda : run_sqlalchemy(),
        rounds=ROUNDS,
        iterations=ITERATIONS
    )

def test_pypika(benchmark):
    benchmark.pedantic(
        lambda : run_pypika(),
        rounds=ROUNDS,
        iterations=ITERATIONS
    )

def test_peewee(benchmark):
    benchmark.pedantic(
        lambda : run_peewee(),
        rounds=ROUNDS,
        iterations=ITERATIONS
    )

