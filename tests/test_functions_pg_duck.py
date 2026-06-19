from parameterized import parameterized

from david8.functions_pg_duck import (
    corr,
    covar_pop,
    covar_samp,
    regr_avgx,
    regr_count,
    regr_intercept,
    regr_r2,
    regr_slope,
    regr_sxx,
    regr_syy,
    stddev_pop,
    stddev_samp,
    var_pop,
    var_samp,
)
from david8.protocols.sql import OverClauseProtocol
from tests.base_test import BaseTest


class TestFunctionsPgDuck(BaseTest):
    @parameterized.expand([
        (
            var_pop('salary').over(partition_by=['dept'], order_by=['date']),
            'SELECT var_pop(salary) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            var_samp('salary').over(partition_by=['dept'], order_by=['date']),
            'SELECT var_samp(salary) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            stddev_pop('salary').over(partition_by=['dept'], order_by=['date']),
            'SELECT stddev_pop(salary) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            stddev_samp('salary').over(partition_by=['dept'], order_by=['date']),
            'SELECT stddev_samp(salary) OVER (PARTITION BY dept ORDER BY date)',
        ),
    ])
    def test_1_arg_fn(self, fn: OverClauseProtocol, exp_sql: str):
        self.assertEqual(BaseTest.qb.select(fn).get_sql(), exp_sql)

    @parameterized.expand([
        (
            corr('salary', 'bonus').over(partition_by=['dept'], order_by=['date']),
            'SELECT corr(salary, bonus) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            covar_pop('salary', 'bonus').over(partition_by=['dept'], order_by=['date']),
            'SELECT covar_pop(salary, bonus) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_slope('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_slope(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_r2('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_r2(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_sxx('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_sxx(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_syy('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_syy(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_avgx('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_avgx(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_count('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_count(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            regr_intercept('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT regr_intercept(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
        (
            covar_samp('salary', 'experience').over(partition_by=['dept'], order_by=['date']),
            'SELECT covar_samp(salary, experience) OVER (PARTITION BY dept ORDER BY date)',
        ),
    ])
    def test_2_arg_fn(self, fn: OverClauseProtocol, exp_sql: str):
        self.assertEqual(BaseTest.qb.select(fn).get_sql(), exp_sql)
