from david8 import get_qb
from david8.agg_functions import avg, count, max_, min_, sum_
from david8.dialects import ClickhouseDialect
from david8.logical_operators import and_, or_, xor
from david8.predicates import eq
from tests.base_test import BaseTest

_qb = get_qb(ClickhouseDialect())

class TestAggFunctions(BaseTest):

    def test_agg_functions(self):
        query = (
            _qb
            .select('*')
            .from_table('test')
            .having(eq(count('*'), 1))
        )

        for expr in [
            eq(count('name'), 2),
            eq(max_('price'), 1000),
            eq(min_('age'), 27),
            eq(sum_('money'), 100),
            eq(avg('success'), 99),
            eq(count('name', True), 3),
            eq(max_('price', True), 2000),
            eq(min_('age', True), 33),
            eq(sum_('money', True), 200),
            eq(avg('success', True), 299),
        ]:
            query.having(expr)

        sql = query.get_sql()
        self.assertEqual(
            sql,
            'SELECT * FROM test HAVING count(*) = 1 AND count(name) = 2 AND max(price) = 1000 AND min(age) = 27 AND '
            'sum(money) = 100 AND avg(success) = 99 AND count(DISTINCT name) = 3 AND max(DISTINCT price) = 2000 AND '
            'min(DISTINCT age) = 33 AND sum(DISTINCT money) = 200 AND avg(DISTINCT success) = 299'
        )

    def test_agg_logical_operators(self):
        query = (
            _qb
            .select('*')
            .from_table('test')
            .having(
                or_(
                    eq(count('name'), 2),
                    eq(max_('price'), 1000),
                    and_(
                        eq(min_('age'), 27),
                        eq(sum_('money'), 100),
                    ),
                    xor(
                        eq(avg('success'), 99),
                        eq(avg('happiness'), 101),
                    )
                )
            )
        )

        sql = query.get_sql()
        self.assertEqual(sql, 'SELECT * FROM test HAVING (count(name) = 2 OR max(price) = 1000 OR (min(age) = 27 '
                              'AND sum(money) = 100) OR (avg(success) = 99 XOR avg(happiness) = 101))')
