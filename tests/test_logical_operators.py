from parameterized import parameterized

from david8.expressions import false, true
from david8.logical_operators import and_, not_, or_, xor
from david8.predicates import eq
from david8.protocols.sql import LogicalOperatorProtocol
from tests.base_test import BaseTest


class TestLogicalOperators(BaseTest):
    def test_or(self):
        query = (
            self.qb
            .select('*')
            .from_table('logical_operators')
            .where(
                or_(
                    eq('col1', 1),
                    eq('col1', 2),
                    xor(
                        eq('col2', 3),
                        eq('col2', 4),
                    ),
                ),
                eq('col3', 5),
            )
         )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM logical_operators WHERE (col1 = %(p1)s OR col1 = %(p2)s OR (col2 = %(p3)s '
            'XOR col2 = %(p4)s)) AND col3 = %(p5)s'
        )

        self.assertEqual(query.get_parameters(), {'p1': 1, 'p2': 2, 'p3': 3, 'p4': 4, 'p5': 5})

    def test_xor(self):
        query = (
            self.qb
            .select('*')
            .from_table('logical_operators')
            .where(
                xor(
                    eq('col1', 1),
                    eq('col1', 2),
                    or_(
                        eq('col2', 3),
                        eq('col2', 4),
                    ),
                ),
                eq('col3', 5),
            )
         )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM logical_operators WHERE (col1 = %(p1)s XOR col1 = %(p2)s XOR '
            '(col2 = %(p3)s OR col2 = %(p4)s)) AND col3 = %(p5)s'
        )

        self.assertEqual(query.get_parameters(), {'p1': 1, 'p2': 2, 'p3': 3, 'p4': 4, 'p5': 5})

    def test_and(self):
        query = (
            self.qb
            .select('*')
            .from_table('logical_operators')
            .where(
                or_(
                    and_(
                        eq('col1', 1),
                        eq('col2', 2),
                        eq('col3', 3),
                    ),
                    eq('col4', 4),
                ),
                eq('col3', 5),
            )
         )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM logical_operators WHERE ((col1 = %(p1)s AND col2 = %(p2)s AND '
            'col3 = %(p3)s) OR col4 = %(p4)s) AND col3 = %(p5)s'
        )

        self.assertEqual(query.get_parameters(), {'p1': 1, 'p2': 2, 'p3': 3, 'p4': 4, 'p5': 5})

    @parameterized.expand([
        (
            not_('column_name'),
            'SELECT NOT column_name',
            'SELECT NOT "column_name"',
            {}
        ),
        (
            not_(true()),
            'SELECT NOT TRUE',
            'SELECT NOT TRUE',
            {}
        ),
        (
            not_(false()),
            'SELECT NOT FALSE',
            'SELECT NOT FALSE',
            {}
        ),
    ])
    def test_not(self, logical: LogicalOperatorProtocol, exp_sql: str, exp_sql2: str, exp_params: dict) -> None:
        query = BaseTest.qb.select(logical)
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)

        query = BaseTest.qb_w.select(logical)
        self.assertEqual(query.get_sql(), exp_sql2)
        self.assertEqual(query.get_parameters(), exp_params)
