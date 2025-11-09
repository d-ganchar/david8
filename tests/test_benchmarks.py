def run_one():
    pass

def run_two():
    pass


def test_one(benchmark):
    benchmark(lambda : run_one())


def test_two(benchmark):
    benchmark(lambda : run_two())
