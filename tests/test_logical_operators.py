from david8 import get_qb
from david8.dialects import ClickhouseDialect
from david8.logical_operators import and_, or_, xor
from david8.predicates import eq_val
from tests.base_test import BaseTest

_qb = get_qb(ClickhouseDialect())

class TestLogicalOperators(BaseTest):
    def test_or(self):
        query = (
            _qb
            .select('*')
            .from_table('logical_operators')
            .where(
                or_(
                    eq_val('col1', 1),
                    eq_val('col1', 2),
                    xor(
                        eq_val('col2', 3),
                        eq_val('col2', 4),
                    ),
                ),
                eq_val('col3', 5),
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
            _qb
            .select('*')
            .from_table('logical_operators')
            .where(
                xor(
                    eq_val('col1', 1),
                    eq_val('col1', 2),
                    or_(
                        eq_val('col2', 3),
                        eq_val('col2', 4),
                    ),
                ),
                eq_val('col3', 5),
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
            _qb
            .select('*')
            .from_table('logical_operators')
            .where(
                or_(
                    and_(
                        eq_val('col1', 1),
                        eq_val('col2', 2),
                        eq_val('col3', 3),
                    ),
                    eq_val('col4', 4),
                ),
                eq_val('col3', 5),
            )
         )

        self.assertEqual(
            query.get_sql(),
            'SELECT * FROM logical_operators WHERE ((col1 = %(p1)s AND col2 = %(p2)s AND '
            'col3 = %(p3)s) OR col4 = %(p4)s) AND col3 = %(p5)s'
        )

        self.assertEqual(query.get_parameters(), {'p1': 1, 'p2': 2, 'p3': 3, 'p4': 4, 'p5': 5})
